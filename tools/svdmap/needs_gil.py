"""SVD ingestion that requires the GIL."""

from logging import critical
from pathlib import Path

from .serstor import Storage

from .model import Address, AddressSpan, MemoryMap, Value
from .parallelization import Result

try:
    from concurrent.futures import ProcessPoolExecutor, as_completed

    from svdsuite import Process
    from svdsuite.model import AccessType, Device

except ImportError:
    critical(
        "svdmap requires the optional 'svdsuite' dependency to function. "
        "Install svdmap[gil] or ensure 'svdsuite' is installed."
    )
    raise


def build_memory_map(device: Device) -> MemoryMap:
    """Build the memory map from an SVD device."""

    memory_map = MemoryMap()
    for peripheral in device.peripherals:
        for register in peripheral.registers:
            if register.access not in (
                AccessType.READ_ONLY,
                AccessType.READ_WRITE,
                AccessType.READ_WRITE_ONCE,
            ):
                continue
            if register.base_address > 0xFFFF_FFFF:
                raise AttributeError(
                    "Found a register with base address > 0xFFFF_FFFF. "
                    "This is likely an error."
                )
            start = Address(register.base_address, 0)
            size = Address(0, register.size)
            value = Value(
                AddressSpan(start, size), register.reset_value, register.reset_mask
            )
            if register.access in (
                AccessType.READ_ONLY,
                AccessType.READ_WRITE,
                AccessType.READ_WRITE_ONCE,
            ):
                memory_map.add_read(value)
            if register.access in (
                AccessType.WRITE_ONLY,
                AccessType.READ_WRITE,
                AccessType.READ_WRITE_ONCE,
                AccessType.WRITE_ONCE,
            ):
                memory_map.add_written(value)
    return memory_map


def ingest_file(input_file: Path) -> Result[MemoryMap]:
    """Process an SVD file."""

    @Result.contained
    def build_map(input_file: Path) -> MemoryMap:
        """Build the memory map from the input file."""
        process = Process.from_svd_file(str(input_file))
        device = process.get_processed_device()
        return build_memory_map(device)

    return build_map(input_file)


def ingest(input_dir: Path, out: Path, timeout: int | None = None) -> None:
    """Ingest a directory of SVD files."""

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory {input_dir} does not exist.")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory {input_dir} is not a directory.")

    storage = Storage(out)
    all_svds = {p for p in input_dir.glob("**/*") if p.suffix in {".svd", ".xml"}}
    svds = {p for p in all_svds if str(p) not in storage}

    if len(all_svds) != len(svds):
        print(f"Skipping {len(all_svds) - len(svds)} cached SVDs.")

    completed = 0
    errors = 0
    with_warnings = 0
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(ingest_file, svd) for svd in svds]
        try:
            for future in as_completed(futures, timeout=timeout):
                completed += 1
                result = future.result()
                if not result.success:
                    errors += 1
                elif result.warnings:
                    with_warnings += 1
                print(
                    f"{completed}/{len(svds)}, "
                    f"{with_warnings} "
                    f"({with_warnings / completed * 100:04.1f}%) "
                    "with warnings, "
                    f"{errors} failed ({errors / completed * 100:04.1f}%).",
                    end="\r",
                )
                svd = result.args[0]
                assert isinstance(svd, Path)
                storage[str(svd)] = result
        except TimeoutError:
            print()
            print(f"Timeout after {timeout} seconds.")
            executor.shutdown(wait=False, cancel_futures=True)
        else:
            print()

    print("Finalizing...")
    storage.export_tar()
    print(
        f"Completed {completed} files with {errors} errors. {len(svds) - completed} "
        "timed out."
    )

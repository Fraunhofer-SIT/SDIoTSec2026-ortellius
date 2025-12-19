"""main routine"""

import argparse
from pathlib import Path

from . import check_storage, make_shadows
from .needs_gil import ingest
from .parallelization import die


def run() -> None:
    """main routine"""

    parser = argparse.ArgumentParser(description="Extract memory maps from SVD files.")
    subparsers = parser.add_subparsers()
    parser_ingest = subparsers.add_parser(
        "ingest", help="ingest a directory of SVD files"
    )
    parser_ingest.add_argument(
        "input_dir", type=Path, help="Path to directory containing SVD files."
    )
    parser_ingest.add_argument("out", type=Path, help="Name of the output file.")
    parser_ingest.add_argument(
        "--timeout", type=int, default=None, help="Timeout in seconds."
    )
    parser_ingest.set_defaults(func=ingest)

    parser_check = subparsers.add_parser(
        "check", help="check generated SVD storage for errors"
    )
    parser_check.add_argument("prefix", type=Path, help="Path to the storage file.")
    parser_check.set_defaults(func=check_storage)

    parser_make_shadows = subparsers.add_parser(
        "make-shadows", help="create shadow files for all memory maps in storage"
    )
    parser_make_shadows.add_argument(
        "prefix", type=Path, help="Path to the storage file."
    )
    parser_make_shadows.add_argument(
        "output_prefix", type=Path, help="Path to the output storage file."
    )
    parser_make_shadows.add_argument(
        "output_dir",
        type=Path,
        nargs="?",
        default=None,
        help="Path to the output directory.",
    )
    parser_make_shadows.set_defaults(func=make_shadows)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    func = args.func
    params = vars(args)
    del params["func"]
    func(**params)

    die()


run()

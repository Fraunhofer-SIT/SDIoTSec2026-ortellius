from pathlib import Path
import sys

from svdmap.serstor import Storage
from svdmap.model import Shadow
from build_access_maps import AnalysisResult
from logging import info


def _print_ranking(ranking: list[tuple[str, float]]) -> str:
    out = ""

    last_score: float | None = None
    rank = 1
    with_this_rank = 0
    for name, s in ranking:
        if s != last_score:
            last_score = s
            if with_this_rank > 0:
                out += f"{with_this_rank} devices with rank #{rank-1}\n"
            out += f"Rank #{rank}: (score {s}, normalized score {s/ranking[0][1]})\n"
            rank += 1
            with_this_rank = 0
        with_this_rank += 1

        out += f"\t{name}\n"

    if with_this_rank > 0:
        out += f"{with_this_rank} devices with rank #{rank}"

    return out


def rank_shadow_jaccard(device_shadow: Path, firmware_shadow: Path) -> str:
    """
    Rank all known devices by Shadow Jaccard similarity to the given memory dump.
    """
    with Storage(device_shadow) as storage:
        shadow_base = [storage.get_and_unserialize(name, Shadow) for name in storage]
    firmware = AnalysisResult.model_validate_json(firmware_shadow.read_text())

    ranks: dict[str, float] = {}
    for shadow in shadow_base:
        intersection = len(shadow.read & firmware.read) + len(
            shadow.write & firmware.write
        )
        union = len(shadow.read | firmware.read) + len(shadow.write | firmware.write)
        similarity = intersection / union if union > 0 else 0.0
        ranks[shadow.name] = similarity

    info("Sorting by similarity...")
    ranking = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
    return _print_ranking(ranking)


def main(outdir: Path, kb_dir: Path) -> None:
    for access_map in outdir.rglob("**/*.json"):
        print(f"Ranking access map {access_map}...")
        (ranks_dir := access_map.with_suffix("")).mkdir(exist_ok=True)
        for shadow_file in kb_dir.glob("shadow_maps*.tar.gz"):
            print(f"  Using shadow map {shadow_file}...")

            (ranks_dir / f"ranking_using_{shadow_file.stem}.txt").write_text(
                rank_shadow_jaccard(shadow_file, access_map)
            )


main(Path(sys.argv[1]), Path(sys.argv[2]))

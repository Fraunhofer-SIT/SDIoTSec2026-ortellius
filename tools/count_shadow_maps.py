from pathlib import Path
import sys

from svdmap.model import Shadow
from svdmap.serstor import Storage


def count_shadow_maps(knowledge_base: Path) -> None:
    """
    Determine number of shadow maps and other stats in the given knowledge base.
    """

    storage = Storage(knowledge_base)
    print(f"Total shadow maps: {len(storage)}")

    equivalence_groups: dict[int, list[Shadow]] = {}

    for svd in storage:
        shadow_map = storage.get_and_unserialize(svd, Shadow)
        group_id = hash((frozenset(shadow_map.read), frozenset(shadow_map.write)))
        if group_id not in equivalence_groups:
            equivalence_groups[group_id] = []
        equivalence_groups[group_id].append(shadow_map)

    # check equivalence groups
    for group in equivalence_groups.values():
        base = group[0]
        for shadow_map in group[1:]:
            assert base.read == shadow_map.read
            assert base.write == shadow_map.write

    # check that sizes add up
    assert sum(len(g) for g in equivalence_groups.values()) == len(storage)

    print(f"Total equivalence groups: {len(equivalence_groups)}")

    largest_group = max(equivalence_groups.values(), key=len)
    print(f"Largest group size: {len(largest_group)}")
    for i, shadow_map in enumerate(largest_group):
        print(f"  Shadow map {i}: {shadow_map.name}")


count_shadow_maps(Path(sys.argv[1]))

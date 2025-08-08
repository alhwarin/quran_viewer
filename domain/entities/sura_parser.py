from typing import List, Tuple
from domain.entities.sura_entity import SuraEntity

def parse_sura_list(raw_sura_data: List[Tuple[int, int, int, str, str, str, str, int, int]]) -> List[SuraEntity]:
    """
    Convert raw sura data into a list of SuraEntity instances.

    Expected raw data format per entry:
        (id, ayas, start, name, ename, meaning, type, order, rukus)
    """
    result = []
    for entry in raw_sura_data:
        try:
            id, ayas, start, name, ename, *_ = entry  # ignore extra fields
            result.append(SuraEntity(id=id, start=start, name=name, ename=ename, ayas=ayas))
        except (ValueError, TypeError) as e:
            print(f"[parse_sura_list] Skipped invalid entry {entry}: {e}")
    return result

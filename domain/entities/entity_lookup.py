from typing import List, Optional
from domain.entities.sura_entity import SuraEntity
from domain.entities.reciter_entity import ReciterEntity

def get_sura_by_name(sura_list: List[SuraEntity], name: str) -> Optional[SuraEntity]:
    return next((sura for sura in sura_list if sura.name == name or sura.ename == name), None)

def get_reciter_by_name(reciter_list: List[ReciterEntity], name: str) -> Optional[ReciterEntity]:
    return next((reciter for reciter in reciter_list if reciter.name == name or reciter.ename == name), None)


def get_sura_by_id(sura_list: List[SuraEntity], sura_id: int) -> Optional[SuraEntity]:
    """Find a sura in the list by its ID."""
    return next((sura for sura in sura_list if sura.id == sura_id), None)

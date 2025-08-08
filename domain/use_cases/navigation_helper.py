from typing import List, Optional
from domain.entities.page_entity import PageEntity
from domain.entities.sura_entity import SuraEntity

def find_page_by_sura_id(pages: List[PageEntity], sura_id: int) -> Optional[PageEntity]:
    return next((p for p in pages if sura_id in p.sura_id_list), None)

def find_first_sura_on_page(pages: List[PageEntity], suras: List[SuraEntity], page_id: int) -> Optional[SuraEntity]:
    page = next((p for p in pages if p.id == page_id), None)
    if not page or not page.sura_id_list:
        return None
    return next((s for s in suras if s.id == page.first_sura_id()), None)

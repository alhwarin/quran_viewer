#domain/use_cases/load_quran_page_use_case.py

from domain.entities.page_entity import PageEntity
from domain.repository_interfaces.quran_repository_interface import IQuranRepository
class LoadQuranPageUseCase:
    def __init__(self, repository: IQuranRepository):
        self.repository = repository

    def execute(self, page: PageEntity):
        # Get the page text (list of ayas)
        ayas = self.repository.get_page_text(page)
    

        # Get sura info for each sura_id in the page
        sura_info_list = [
            self.repository.get_sura_info(sura_id) for sura_id in page.sura_id_list
        ]
    

        # Return ayas, list of sura_info, and the PageEntity (if needed)
        return ayas, sura_info_list


    def get_first_page_for_sura(self, sura_id: int):
        return self.repository.get_first_page_for_sura(sura_id)
    
    def get_page_info(self, page_id: int):
        return self.repository.get_page_info(page_id)

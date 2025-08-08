#domain/use_cases/get_data_list_use_case.py
from typing import List
from domain.entities.reciter_entity import ReciterEntity
from domain.entities.sura_entity import SuraEntity
from domain.entities.page_entity import PageEntity
from domain.repository_interfaces.quran_repository_interface import IQuranRepository
# Optional parser imports if needed, e.g., parse_sura_list

class GetDataListUseCase:
    def __init__(self, repository: IQuranRepository):
        self.repository = repository

    def get_reciter_list(self) -> List[ReciterEntity]:
        """
        Fetch and return list of ReciterEntity from repository.
        """
        raw_data = self.repository.get_reciter_list()
        return raw_data

    def get_sura_list(self) -> List[SuraEntity]:
        """
        Fetch and return list of SuraEntity from repository.
        """
        raw_data = self.repository.get_sura_list()
        return raw_data

    def get_page_list(self) -> List[PageEntity]:
        """
        Fetch and return list of PageEntity from repository.
        """
        raw_data = self.repository.get_page_list()
        return raw_data

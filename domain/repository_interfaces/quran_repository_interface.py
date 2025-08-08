#domain/repository_interfaces/quran_repository_interface.py
from domain.entities.page_entity import PageEntity
from abc import ABC, abstractmethod
from PyQt5.QtGui import QColor
from typing import List, Dict


class IQuranRepository(ABC):
    @abstractmethod
    def get_sura_list(self):
        pass

    @abstractmethod
    def get_page_list(self, sura_id: int):
        pass

    @abstractmethod
    def get_aya_list(self, sura_id: int):
        pass

    @abstractmethod
    def get_quran_text(self, sura_id: int, aya_id: int = 0):
        pass

    @abstractmethod
    def get_reciter_list(self):
        pass

    @abstractmethod
    def get_sura_playlist(self, sura_id: int, reciter: str):
        pass

    @abstractmethod
    def get_page_playlist(self, page_id: int, reciter: str):
        pass

    # New methods for pagination & pages table
    @abstractmethod
    def get_page_info(self, page_num: int):
        """Return dictionary with page info like sura, start aya, ayas_count for given page number"""
        pass

    @abstractmethod
    def get_quran_text_range(self, sura_id: int, start_aya: int, count: int):
        """Return list of ayas for the given sura, starting from start_aya, limited to count"""
        pass

    @abstractmethod
    def get_page_text(self, page: PageEntity):
        """Return list of ayas for the given sura, starting from start_aya, limited to count"""
        pass

    
    @abstractmethod
    def get_first_page_for_sura(self, sura_id: int): pass  # <-- ADD THIS

    @abstractmethod
    def get_sura_info(self, sura_id: int): pass

    @abstractmethod
    def set_font_color(self, color: QColor) -> None:
        pass

    @abstractmethod
    def get_font_color(self) -> QColor:
        pass

    @abstractmethod
    def set_bg_color(self, color: QColor) -> None:
        pass

    @abstractmethod
    def get_bg_color(self) -> QColor:
        pass

    @abstractmethod
    def set_highlight_color(self, color: QColor) -> None:
        pass

    @abstractmethod
    def get_highlight_color(self) -> QColor:
        pass

    @abstractmethod
    def set_font_size(self, size: int) -> None:
        pass

    @abstractmethod
    def get_font_size(self) -> int:
        pass

    @abstractmethod
    def generate_html(self, sura_id: int, sura_info: Dict, quran_data: List[Dict]) -> str:
        pass


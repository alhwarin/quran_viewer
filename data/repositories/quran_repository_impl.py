#data/repositories/quran_repository_impl.py
from PyQt5.QtGui import QColor
from data.datasources.quran_local_datasource import QuranLocalDataSource
from domain.repository_interfaces.quran_repository_interface import IQuranRepository
from domain.entities.page_entity import PageEntity
from data.repositories.display_renderer import DisplayRenderer

class QuranRepositoryImpl(IQuranRepository):
    def __init__(self, config_path):
        self.local = QuranLocalDataSource(config_path)
        self.renderer = DisplayRenderer()

    # Quran Data Access Methods
    def get_sura_list(self):
        return self.local.get_sura_list()
    
    def get_page_list(self):
        return self.local.get_page_list()

    def get_aya_list(self, sura_id):
        return self.local.get_aya_list(sura_id)

    def get_quran_text(self, sura_id, aya_id=0):
        return self.local.get_quran_text(sura_id, aya_id)

    def get_reciter_list(self):
        return self.local.get_reciter_list()

    def get_sura_playlist(self, sura_id, reciter):
        return self.local.get_sura_playlist(sura_id, reciter)
    
    def get_page_playlist(self, page_id, reciter):
        return self.local.get_page_playlist(page_id, reciter)

    def get_page_info(self, page_num):
        return self.local.get_page_info(page_num)

    def get_quran_text_range(self, sura_id, start_aya, count):
        return self.local.get_quran_text_range(sura_id, start_aya, count)

    def get_page_text(self, page: PageEntity):
        return self.local.fetch_page_text(page)

    def get_first_page_for_sura(self, sura_id: int):
        return self.local.get_first_page_for_sura(sura_id)

    def get_sura_info(self, sura_id: int):
        return self.local.get_sura_info(sura_id)

    @property
    def model(self):
        return self.local

    # Display Rendering Methods
    def set_font_color(self, color: QColor): 
        self.renderer.set_font_color(color)

    def get_font_color(self) -> QColor: 
        return self.renderer.get_font_color()

    def set_bg_color(self, color: QColor): 
        self.renderer.set_bg_color(color)

    def get_bg_color(self) -> QColor: 
        return self.renderer.get_bg_color()

    def set_highlight_color(self, color: QColor): 
        self.renderer.set_highlight_color(color)

    def get_highlight_color(self) -> QColor: 
        return self.renderer.get_highlight_color()

    def set_font_size(self, size: int): 
        self.renderer.set_font_size(size)

    def get_font_size(self) -> int: 
        return self.renderer.get_font_size()  
    
    def generate_html(self, sura_id, sura_info, quran_data) -> str:
        return self.renderer.generate_html(sura_id, sura_info, quran_data)
        #return self.renderer.generate_html_new(
        #    sura_id
        #)



    
    def render_page(self, page_num, sura_info, quran_data) -> str:
        return self.generate_html(page_num, sura_info, quran_data)

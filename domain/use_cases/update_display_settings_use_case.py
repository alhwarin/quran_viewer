#domain/use_cases/upate_display_settings_use_case.py
from domain.repository_interfaces.quran_repository_interface import IQuranRepository
from PyQt5.QtGui import QColor
class UpdateDisplaySettingsUseCase:
    def __init__(self, renderer: IQuranRepository):
        self.renderer = renderer

    def execute(self, sura_id: int, sura_info_list: list[dict], quran_data: list):
        return self.renderer.generate_html(sura_id, sura_info_list, quran_data)

    def set_font_size(self, font_size: int):
        """Updates font size in the renderer and web view."""
        self.renderer.set_font_size(font_size)
        #self._run_js(f"setFontSize({font_size});")

    def set_font_color(self, color: QColor):
        """Updates font color in the renderer and web view."""
        self.renderer.set_font_color(color)
        #self._run_js(f"setFontColor('{color.name()}');")

    def set_bg_color(self, color: QColor):
        """Updates background color in the renderer and web view."""
        self.renderer.set_bg_color(color)
        #self._run_js(f"setBackgroundColor('{color.name()}');")

    def set_highlight_color(self, color: QColor):
        """Updates highlight color in the renderer and web view."""
        self.renderer.set_highlight_color(color)
        #self._run_js(f"setHighlightColor('{color.name()}');")

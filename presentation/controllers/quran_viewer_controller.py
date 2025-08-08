#presentation/controllers/quran_viewer_controller.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
from PyQt5.QtGui import QColor

from domain.use_cases.get_data_list_use_case import GetDataListUseCase
from presentation.events.quran_events import (
    LoadFirstPageOfSuraEvent,
    LoadPageEvent,
    LoadNextPageEvent,
    LoadPreviousPageEvent,
    SuraListRequestEvent,
    ReciterListRequestEvent,
    PageListRequestEvent,
    HighlightAyaEvent
)
from presentation.events.settings_events import (
    FontSizeChangedEvent,
    FontColorChangedEvent,
    BackgroundColorChangedEvent,
    HighlightColorChangedEvent
)
from domain.entities.page_entity import PageEntity

@dataclass
class PageData:
    quran_data: Dict[str, Any]
    sura_info: Dict[str, Any]


class QuranViewerController:
    MAX_PAGES = 604
    MIN_PAGES = 1

    def __init__(
        self,
        load_page_uc: Any,
        quran_state: Any,
        get_data_list_uc: Optional[GetDataListUseCase] = None,
        display_update_uc: Optional[Any] = None,
    ):
        self.load_page_uc = load_page_uc
        self.display_update_uc = display_update_uc
        self.get_data_list_use_case = get_data_list_uc
        self.state = quran_state

        self.current_page_id: int = self.MIN_PAGES
        self.current_sura_id: int = 1
        self.current_page : PageEntity

    # --- Event handling for Quran navigation ---
    def handle_event(self, event: Union[
        LoadFirstPageOfSuraEvent,
        LoadPageEvent,
        LoadNextPageEvent,
        LoadPreviousPageEvent,
        SuraListRequestEvent,
        ReciterListRequestEvent,
        PageListRequestEvent,
        HighlightAyaEvent,
        FontSizeChangedEvent,
        FontColorChangedEvent,
        BackgroundColorChangedEvent,
        HighlightColorChangedEvent
    ]) -> None:
        """Dispatch Quran navigation events to appropriate handlers."""
        try:
            if isinstance(event, LoadFirstPageOfSuraEvent):
                self._handle_load_first_page_of_sura_event(event.sura_id)
            elif isinstance(event, LoadPageEvent):
                self._handle_page_load(event.page_id)
            elif isinstance(event, LoadNextPageEvent):
                self._handle_next_page_event()
            elif isinstance(event, LoadPreviousPageEvent):
                self._handle_previous_page_event()
            elif isinstance(event, SuraListRequestEvent):
                self._handle_sura_list_request()
            elif isinstance(event, ReciterListRequestEvent):
                self._handle_reciter_list_request()
            elif isinstance(event, PageListRequestEvent):
                self._handle_page_list_request()
            elif isinstance(event, HighlightAyaEvent):
                self._handle_highlight_aya_request(event.aya_id)
            if isinstance(event, FontSizeChangedEvent):
                self.set_font_size(event.font_size)

            elif isinstance(event, FontColorChangedEvent):
                self.set_font_color(event.color)

            elif isinstance(event, BackgroundColorChangedEvent):
                self.set_bg_color(event.color)

            elif isinstance(event, HighlightColorChangedEvent):
                self.set_highlight_color(event.color)
            else:
                    self._log_error(f"Unhandled event type: {type(event).__name__}")
        except Exception as e:
            self._log_error(f"Error handling event {type(event).__name__}: {e}")

    def _handle_load_first_page_of_sura_event(self, sura_id: int) -> None:
        self.current_sura_id = sura_id
        self.current_page = self.load_page_uc.get_first_page_for_sura(sura_id)
        self._load_page()

    def _handle_page_load(self, page_id: int) -> None:
        if self.MIN_PAGES <= page_id <= self.MAX_PAGES:
            self.current_page = self.load_page_uc.get_page_info(page_id)
            self._load_page()
        else:
            self._log_error(f"Page {page_id} is out of range.")

    def _handle_next_page_event(self) -> None:
        if self.current_page.id < self.MAX_PAGES:
            self.current_page.id += 1
            self.current_page = self.load_page_uc.get_page_info(self.current_page.id)
            self._load_page()

    def _handle_previous_page_event(self) -> None:
        if self.current_page.id > self.MIN_PAGES:
            self.current_page.id -= 1
            self.current_page = self.load_page_uc.get_page_info(self.current_page.id)
            self._load_page()

    def _handle_sura_list_request(self) -> None:
        try:
            self.state.sura_list = self.get_data_list_use_case.get_sura_list()
        except Exception as e:
            self._log_error(f"Error fetching sura list: {e}")

    def _handle_page_list_request(self) -> None:
        try:
            self.state.page_list = self.get_data_list_use_case.get_page_list()
           
        except Exception as e:
            self._log_error(f"Error fetching page list: {e}")

    def _handle_reciter_list_request(self) -> None:
        try:
            self.state.reciter_list = self.get_data_list_use_case.get_reciter_list()
        except Exception as e:
            self._log_error(f"Error fetching reciter list: {e}")

    def _handle_highlight_aya_request(self, aya_id: int )-> None:
        try:
            #self.state.reciter_list = self.get_data_list_use_case.get_reciter_list()
            self.state.js_script= (f"highlightAya('{aya_id}');")
        except Exception as e:
            self._log_error(f"Error highlighting aya: {e}")


    def _load_page(self) -> None:
        """
        Loads and displays the specified Quran page.
        Fetches ayas and sura info, generates HTML, and updates the view/state.
        """
        try:
            # Update internal page state
            print(f"[INFO] Loading page ID: {self.current_page.id}")

            # Fetch ayas and sura info from use case
            ayas, sura_info = self.load_page_uc.execute(self.current_page)
            print(f"[DEBUG] Loaded {len(ayas)} ayas for page {self.current_page.id}")

            # Generate HTML from fetched data
            self.state.html_text = self.display_update_uc.execute(self.current_page.id, sura_info, ayas)
            print(f"[DEBUG] Generated HTML for page {self.current_page.id} (length: {len(self.state.html_text)} chars)")

            # Update application state
            self.state.set_page(self.current_page)
            print(f"[INFO] Page {self.current_page.id} successfully loaded.")

        except Exception as e:
            self._log_error(f"[ERROR] Failed to load page {self.current_page.id}: {e}")




    # --- Text rendering controls ---

    def render_page(self, page_num, sura_info, quran_data):
        """Generates HTML content and sends it to the web view."""
        self.state.html_text = self.display_update_uc.execute(page_num, sura_info, quran_data)

    def highlight_aya(self, aya_id: int):
        """Highlights the specified Aya in the web view."""
        self.state.js_script= (f"highlightAya('{aya_id}');")

    def set_font_size(self, font_size: int):
        """Updates font size in the renderer and web view."""
        self.display_update_uc.set_font_size(font_size)
        self.state.js_script= (f"setFontSize({font_size});")

    def set_font_color(self, color: QColor):
        """Updates font color in the renderer and web view."""
        self.display_update_uc.set_font_color(color)
        self.state.js_script= (f"setFontColor('{color.name()}');")

    def set_bg_color(self, color: QColor):
        """Updates background color in the renderer and web view."""
        self.display_update_uc.set_bg_color(color)
        self.state.js_script= (f"setBackgroundColor('{color.name()}');")

    def set_highlight_color(self, color: QColor):
        """Updates highlight color in the renderer and web view."""
        self.display_update_uc.set_highlight_color(color)
        self.state.js_script= (f"setHighlightColor('{color.name()}');")


    def _log_error(self, message: str) -> None:
        print(f"[ERROR] {message}")

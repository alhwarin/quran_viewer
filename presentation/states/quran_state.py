#presentation/states/quran_state.py
from typing import List, Optional
from presentation.states.state_manager import StateManager  # Central manager
from domain.entities.sura_entity import SuraEntity
from domain.entities.reciter_entity import ReciterEntity
from domain.entities.page_entity import PageEntity


class QuranState:
    def __init__(self):
        # --- Unique source ID for centralized observer notification ---
        self._source_id = "quran"

        # --- Quran state ---
        self._current_page_id: int = 1
        self._current_sura_id: int = 1
        self._sura_list: List[SuraEntity] = []
        self._page_list: List[PageEntity] = []
        self._reciter_list: List[ReciterEntity] = []
        self._current_page: Optional[PageEntity] = None

        # --- Audio player state ---
        self._is_playing: bool = False
        self._current_aya_number: Optional[int] = None
        self._current_reciter_name: Optional[str] = None
        self._current_sura_name: Optional[str] = None
        self._current_page_name: Optional[str] = None
        self._volume: int = 50
        self._html_text: Optional[str] = None
        self._js_script : Optional[str] = None

    # -----------------------
    # Page Handling
    # -----------------------

    def set_page(self, page: PageEntity):
        self._current_page = page
        self._notify("current_page")

    @property
    def current_page(self) -> Optional[PageEntity]:
        return self._current_page

    # -----------------------
    # Quran-related properties
    # -----------------------

    @property
    def current_page_id(self) -> int:
        return self._current_page_id or 1

    @current_page_id.setter
    def current_page_id(self, value: int):
        if value < 1:
            raise ValueError("current_page_id must be >= 1")
        self._current_page_id = value
        self._notify("current_page_id")

    @property
    def current_sura_id(self) -> int:
        return self._current_sura_id or 1

    @current_sura_id.setter
    def current_sura_id(self, value: int):
        if value < 1:
            raise ValueError("current_sura_id must be >= 1")
        self._current_sura_id = value
        self._notify("current_sura_id")

    @property
    def sura_list(self) -> List[SuraEntity]:
        return self._sura_list

    @sura_list.setter
    def sura_list(self, value: Optional[List[SuraEntity]]):
        self._sura_list = value or []
        self._notify("sura_list")


    @property
    def page_list(self) -> List[PageEntity]:
        return self._page_list

    @page_list.setter
    def page_list(self, value: Optional[List[PageEntity]]):
        self._page_list = value or []
        self._notify("page_list")


    @property
    def reciter_list(self) -> List[ReciterEntity]:
        return self._reciter_list

    @reciter_list.setter
    def reciter_list(self, value: Optional[List[ReciterEntity]]):
        self._reciter_list = value or []
        self._notify("reciter_list")

    # ----------------------------
    # Audio-related state
    # ----------------------------

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    @is_playing.setter
    def is_playing(self, value: bool):
        self._is_playing = value
        self._notify("is_playing")

    @property
    def current_aya_number(self) -> Optional[int]:
        return self._current_aya_number

    @current_aya_number.setter
    def current_aya_number(self, value: Optional[int]):
        self._current_aya_number = value
        self._notify("current_aya_number")

    @property
    def current_reciter_name(self) -> Optional[str]:
        return self._current_reciter_name

    @current_reciter_name.setter
    def current_reciter_name(self, value: Optional[str]):
        self._current_reciter_name = value
        self._notify("current_reciter_name")

    @property
    def current_sura_name(self) -> Optional[str]:
        return self._current_sura_name

    @current_sura_name.setter
    def current_sura_name(self, value: Optional[str]):
        self._current_sura_name = value
        self._notify("current_sura_name")


    @property
    def current_page_name(self) -> Optional[str]:
        return self._current_page_name

    @current_sura_name.setter
    def current_page_name(self, value: Optional[str]):
        self._current_page_name = value
        self._notify("current_page_name")



    @property
    def html_text(self) -> Optional[str]:
        return self._html_text

    @html_text.setter
    def html_text(self, value: Optional[str]):
        self._html_text = value
        self._notify("html_text")

    
    @property
    def js_script(self) -> Optional[str]:
        return self._js_script

    @js_script.setter
    def js_script(self, value: Optional[str]):
        self._js_script = value
        self._notify("js_script")


    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError("Volume must be between 0 and 100")
        self._volume = value
        self._notify("volume")

    # -----------------------
    # Notify via StateManager
    # -----------------------

    def _notify(self, changed_property: str):
        StateManager.notify(self._source_id, changed_property)



    def get_reciter_by_name(self, name: str) -> Optional[ReciterEntity]:
        for reciter in self.reciter_list:
            if reciter.name == name or reciter.ename == name:
                return reciter
        return None

    def get_sura_by_name(self, name: str) -> Optional[SuraEntity]:
        for sura in self.sura_list:
            if sura.name == name or sura.ename == name:
                return sura
        return None
    
    def get_page_by_name(self, name: str) -> Optional[PageEntity]:
        for page in self.page_list:
            display_page_name = f"صفحة {page.id}"
            e_display_page_name = f"Page {page.id}"
            if display_page_name == name or e_display_page_name == name:
                return page
        return None
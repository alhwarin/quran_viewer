
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

from presentation.views.text_renderer_widget import TextRendererWidget
from presentation.views.audio_player_widget import AudioPlayerWidget
from presentation.views.settings_widget import SettingsWidget
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
from presentation.controllers.quran_viewer_controller import QuranViewerController

from presentation.states.state_manager import StateManager  # ✅ Centralized state manager
from presentation.states.quran_state import QuranState
from domain.entities.reciter_entity import ReciterEntity

from domain.entities.entity_lookup import get_sura_by_name, get_reciter_by_name, get_sura_by_id
from domain.use_cases.navigation_helper import find_page_by_sura_id, find_first_sura_on_page




class QuranViewerScreen(QWidget):
    def __init__(self, 
                 event_dispatcher, 
                 quran_state,
                 parent=None):
        super().__init__(parent)

        self.state = quran_state
        StateManager.add_observer("quran", self)  # ✅ Register with StateManager

        self.event_dispatcher = event_dispatcher


        self.sura_selector = QComboBox()
        self.page_selector = QComboBox()
        self.reciter_selector = QComboBox()

        self.sura_selector.currentTextChanged.connect(self.on_sura_changed)
        self.page_selector.currentTextChanged.connect(self.on_page_changed)
        self.reciter_selector.currentTextChanged.connect(self.on_reciter_changed)

        self.text_renderer = TextRendererWidget(self.state, self.event_dispatcher)
        

        self.audio_controls = AudioPlayerWidget(
            self.state,  event_dispatcher,
        )

        self.settings_panel = SettingsWidget(self.event_dispatcher)
        self._init_ui()
        self._load_initial_data()

    def _init_ui(self):
        """Initialize layout and UI controls."""
        layout = QVBoxLayout()
        selection = QHBoxLayout()

        selection.addWidget(QLabel("Sura:"))
        selection.addWidget(self.sura_selector)

        selection.addWidget(QLabel("Page:"))
        selection.addWidget(self.page_selector)

        selection.addWidget(QLabel("Reciter:"))
        selection.addWidget(self.reciter_selector)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self._emit_next_page_event)
        selection.addWidget(next_btn)

        previous_btn = QPushButton("Prev")
        previous_btn.clicked.connect(self._emit_previous_page_event)
        selection.addWidget(previous_btn)

        layout.addLayout(selection, stretch=0)               # No extra space
        layout.addWidget(self.settings_panel, stretch=0)     # Minimal space
        layout.addWidget(self.text_renderer, stretch=1)      # ✅ Take most space
        layout.addWidget(self.audio_controls, stretch=0)     # Minimal space

        self.setLayout(layout)

    def _emit_load_sura_event(self):
        sura_name = self.sura_selector.currentText()
        sura= self.state.get_sura_by_name(sura_name)
        page_name = self.page_selector.currentText()
        page = self.state.get_page_by_name(page_name)
        if sura.id is not None:
            self.event_dispatcher.emit_event(LoadFirstPageOfSuraEvent(sura.id))


    def _emit_load_page_event(self):
        page_name = self.page_selector.currentText()
        page = self.state.get_page_by_name(page_name)
        if page.id is not None:
            self.event_dispatcher.emit_event(LoadPageEvent(page_id= page.id))

    def _emit_next_page_event(self):
        self.event_dispatcher.emit_event(LoadNextPageEvent(self.state.current_page))

    def _emit_previous_page_event(self):
        self.event_dispatcher.emit_event(LoadPreviousPageEvent(self.state.current_page))

    def _emit_highlight_aya_event(self, aya_id: int):
        self.event_dispatcher.emit_event(HighlightAyaEvent(aya_id = aya_id))


    def _load_initial_data(self):
        """Request initial state like sura and reciter lists."""
        self._load_suras()
        self._load_pages()
        self._load_reciters()
        self.event_dispatcher.emit_event(LoadPageEvent(page_id= 1))

    def _load_suras(self):
        self.sura_selector.clear()
        self.event_dispatcher.emit_event(SuraListRequestEvent())

    def _load_pages(self):
        self.page_selector.clear()
        self.event_dispatcher.emit_event(PageListRequestEvent())

    def _load_reciters(self):
        self.reciter_selector.clear()
        self.event_dispatcher.emit_event(ReciterListRequestEvent())

    def on_state_changed(self, source: str, changed_property: str):
        print(f"[STATE] {source} changed: {changed_property}")

        if source != "quran":
            return

        if changed_property == 'sura_list':
            self._update_sura_selector()
        elif changed_property == 'current_page':
            current_page = self.state.current_page
            first_aya_on_page = current_page.start_id
            self._emit_highlight_aya_event(first_aya_on_page)
            display_name = f"صفحة {current_page.id}"
            self.page_selector.setCurrentText(display_name)
        elif changed_property == 'reciter_list':
            self.reciter_list = self.state.reciter_list
            self._update_reciter_selector()

        elif changed_property == 'page_list':
            self.pagelist = self.state.page_list
            self._update_page_selector()

        elif changed_property == 'current_aya_number':
            current_aya = self.state.current_aya_number 
            current_page = self.state.current_page

            if current_aya is not None and current_page:
                first_aya_on_page = current_page.start_id
                last_aya_on_page = current_page.start_id + current_page.ayas_count - 1

                print(f"[DEBUG] current_aya: {current_aya}, first_on_page: {first_aya_on_page}, last_on_page: {last_aya_on_page}")

                if current_aya < first_aya_on_page:
                    print("[DEBUG] Current aya before page start")
                elif current_aya > last_aya_on_page:
                    print("[DEBUG] Current aya after page end")
                else:
                    print(f"[DEBUG] Highlighting aya: {current_aya}")
                    self._emit_highlight_aya_event(current_aya)

                if current_aya == last_aya_on_page +1:
                    print("[INFO] Last Aya reached, loading next page...")
                    self._emit_next_page_event()



    def _update_sura_selector(self):
        self.sura_selector.blockSignals(True)  # 🔇 Temporarily block signals
        self.sura_selector.clear()
        for sura in self.state.sura_list:
            self.sura_selector.addItem(sura.name)
        # Optionally select the first sura by default
        if self.state.sura_list:
            self.sura_selector.setCurrentIndex(0)
            self.state.current_sura_name = self.sura_selector.currentText()
        self.sura_selector.blockSignals(False)  # 🔊 Re-enable signals
    def _update_page_selector(self):
        self.page_selector.blockSignals(True)  # 🔇 Temporarily block signals
        self.page_selector.clear()
        for page in self.state.page_list:
            display_name = f"صفحة {page.id}"
            self.page_selector.addItem(display_name, page.id)

        # Optionally select the current page or default to the first
        if self.state.page_list:
            # Find current index by matching current_page_id (if available)
            current_page_id = self.state.current_page_id
            index = next(
                (i for i, page in enumerate(self.state.page_list) if page.id == current_page_id), 0
            )
            self.page_selector.setCurrentIndex(index)

        self.page_selector.blockSignals(False)  # 🔊 Re-enable signals

    def _update_reciter_selector(self):
        self.reciter_selector.blockSignals(True)  # 🔇 Block signals

        self.reciter_selector.clear()

        for reciter in self.state.reciter_list:
            self.reciter_selector.addItem(reciter.name)

        # Optionally set the first item as selected
        if self.state.reciter_list:
            #self.reciter_selector.currentText()
            self.state.current_reciter_name = self.reciter_selector.currentText()

        self.reciter_selector.blockSignals(False)  # 🔊 Unblock signals

    def closeEvent(self, event):
        StateManager.remove_observer("quran", self)  # ✅ Clean up
        super().closeEvent(event)

    def on_reciter_changed(self, text):
        print(f"Reciter changed to: {text}")
        self.state.current_reciter_name =text
        # Add your logic here

    def on_sura_changed(self, sura_name):
        print(f"Sura changed to: {sura_name}")
        self.state.current_sura_name = sura_name
        sura = get_sura_by_name(self.state.sura_list, sura_name)
        if sura:
            page = find_page_by_sura_id(self.state.page_list, sura.id)
            if page:
                self.state.current_page_id = page.id
                self._update_page_selector()  # Optionally reset page selector
                self.page_selector.setCurrentText(f"صفحة {page.id}")
        
        self._emit_load_sura_event()


    def on_page_changed(self, page_text):
        print(f"Page changed to: {page_text}")

        # Extract page number from string like "صفحة 5"
        try:
            page_id = int(page_text.replace("صفحة ", ""))
        except ValueError:
            print(f"Invalid page format: {page_text}")
            return

        self.state.current_page_id = page_id
        self._emit_load_page_event()
        sura = find_first_sura_on_page(self.state.page_list, self.state.sura_list, page_id)
        if sura:
            self.state.current_sura_name = sura.name
            # Update selector without emitting signal again
            self.sura_selector.blockSignals(True)
            index = self.sura_selector.findText(sura.name)
            if index != -1:
                self.sura_selector.setCurrentIndex(index)
            self.sura_selector.blockSignals(False)
            
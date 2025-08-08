from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt
from presentation.events.audio_events import (
    PlayAudioEvent,
    StopAudioEvent,
    SetVolumeEvent,
    PauseAudioEvent,
    ResumeAudioEvent,
    SeekAudioEvent
)
from presentation.states.quran_state import QuranState
class AudioPlayerWidget(QWidget):
    def __init__(self,  quran_state : QuranState,   event_dispatcher,parent=None):
        super().__init__(parent)
        self.event_dispatcher = event_dispatcher
        self.quran_state = quran_state
        
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        self.play_btn = QPushButton("\u25B6\uFE0F Play")
        self.play_btn.clicked.connect(self._play)

        self.pause_btn = QPushButton("\u23F8 Pause")
        self.pause_btn.clicked.connect(self._pause)

        self.resume_btn = QPushButton("\u23EF Resume")
        self.resume_btn.clicked.connect(self._resume)

        self.stop_btn = QPushButton("\u23F9\uFE0F Stop")
        self.stop_btn.clicked.connect(self._stop)

        self.volume_label = QLabel("\U0001F50A Volume:")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self._change_volume)

        self.seek_label = QLabel("Seek:")
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 100)  # Should be updated based on audio duration
        self.seek_slider.sliderReleased.connect(self._seek_audio)

        layout.addWidget(self.play_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.resume_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.seek_label)
        layout.addWidget(self.seek_slider)

        self.setLayout(layout)

    def _play(self):
        #sura_id = self.sura_selector.currentData()
        sura_name = self.quran_state.current_sura_name
        sura = self.quran_state.get_sura_by_name(sura_name)
        #reciter_name = self.reciter_selector.currentText()
        reciter_name = self.quran_state.current_reciter_name
        aya_id = 1
        reciter = self.quran_state.get_reciter_by_name(reciter_name)
        if reciter.key is not None and sura.id is not None:
            event = PlayAudioEvent(sura_id=sura.id, aya_number=aya_id, reciter_key=reciter.key)
            self.event_dispatcher.emit_event(event)

        else:
            print("[AudioPlayerWidget] Invalid sura or reciter selection")

    def _pause(self):
        event = PauseAudioEvent()
        self.event_dispatcher.emit_event(event)


    def _resume(self):
        event = ResumeAudioEvent()
        self.event_dispatcher.emit_event(event)

    def _stop(self):
        event = StopAudioEvent()
        self.event_dispatcher.emit_event(event)


    def _change_volume(self, value: int):
        event = SetVolumeEvent(volume=value)
        self.event_dispatcher.emit_event(event)


    def _seek_audio(self):
        seek_position = self.seek_slider.value()  # Value from 0 to 100
        event = SeekAudioEvent(position_percent=seek_position)
        self.event_dispatcher.emit_event(event)
  

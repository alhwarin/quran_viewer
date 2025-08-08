#presentation/controllers/audio_player_controller.py
from typing import Optional, Union, Any, List
from domain.entities.reciter_entity import ReciterEntity
from domain.use_cases.get_data_list_use_case import GetDataListUseCase
from presentation.events.audio_events import (
    PlayAudioEvent,
    PauseAudioEvent,
    ResumeAudioEvent,
    StopAudioEvent,
    SeekAudioEvent,
    LoadRecitationForPageEvent,

    SetVolumeEvent
)
from presentation.events.quran_events import ReciterListRequestEvent

class AudioPlayerController:
    def __init__(
        self,
        audio_player: Any,
        state: Any,
        get_data_list_uc: Optional[GetDataListUseCase] = None
    ):
        self.audio_player = audio_player
        self.state = state
        #self.get_reciter_list_use_case = get_reciter_list_uc or GetReciterListUseCase(audio_player.repository)

    def handle_event(self, event: Union[
        PlayAudioEvent,
        PauseAudioEvent,
        ResumeAudioEvent,
        StopAudioEvent,
        SeekAudioEvent,
        LoadRecitationForPageEvent,
        ReciterListRequestEvent,
        SetVolumeEvent
    ]) -> None:
        """Dispatch audio events to appropriate handlers."""
        try:
            if isinstance(event, PlayAudioEvent):
                self._play_audio(event)
            elif isinstance(event, PauseAudioEvent):
                self.audio_player.pause()
            elif isinstance(event, ResumeAudioEvent):
                self.audio_player.resume()
            elif isinstance(event, StopAudioEvent):
                self.audio_player.stop()
            elif isinstance(event, SeekAudioEvent):
                duration = self.audio_player.duration()
                if duration > 0:
                    target_position = int((event.position_percent / 100) * duration)
                    self.audio_player.seek(target_position)
            elif isinstance(event, LoadRecitationForPageEvent):
                self._load_page_audio(event.page_number, event.reciter_id)
            elif isinstance(event, ReciterListRequestEvent):
                self._handle_reciter_list_request()
            elif isinstance(event, SetVolumeEvent):
                 self._handle_set_volume(event.volume)

            else:
                self._log_error(f"Unhandled event type: {type(event).__name__}")
        except Exception as e:
            self._log_error(f"Error handling event {type(event).__name__}: {e}")

    def _play_audio(self, event: PlayAudioEvent) -> None:
        """Play recitation for a given sura_id and aya_id."""
        print(f"event: {event}")

        self.audio_player.load_playlist(event.sura_id, event.reciter_key)
        self.audio_player.play()

    def _load_page_audio(self, page_number: int, reciter_id: Optional[int]) -> None:
        """Play recitations for all ayahs on a given page."""
        self.audio_player.load_page_audio(page_number, reciter_id)

    def _handle_reciter_list_request(self) -> None:
        """Fetch and update the list of available reciters."""
        try:
            reciters: List[ReciterEntity] = self.get_reciter_list_use_case.execute()
            self.state.reciter_list = reciters
        except Exception as e:
            self._log_error(f"Error fetching reciter list: {e}")


    def _handle_set_volume(self, volume) -> None:
        try:
            self.audio_player.set_volume(volume)
        except Exception as e:
            self._log_error(f"Error set volume: {e}")

    def _log_error(self, message: str) -> None:
        """Log error messages (placeholder)."""
        print(f"[ERROR] {message}")

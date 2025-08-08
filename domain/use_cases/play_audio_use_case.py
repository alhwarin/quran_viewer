#domain/use_cases/play_audio_use_case.py
from typing import Optional
from domain.repository_interfaces.audio_player_repository_interface import IAudioPlayer

class PlayAudioUseCase:
    def __init__(self, audio_player: IAudioPlayer, state):
        self.audio_player = audio_player
        self.state = state

    def execute1(self, sura_id: int, reciter: str, start_index: Optional[int] = 0) -> bool:
        """
        Execute audio playback
        Returns True if playback started successfully
        """
        if not self.audio_player.load_playlist(sura_id, reciter):
            return False
            
        self.audio_player.playlist.setCurrentIndex(start_index)
        self.audio_player.play()
        return True
    
    def execute(self, sura_id: int, reciter: str, start_index: int = 0):
        if self.audio_player.load_playlist(sura_id, reciter):
            self.state.current_sura = sura_id
            self.state.current_reciter = reciter
            self.state.current_index = start_index
            self.audio_player.playlist.setCurrentIndex(start_index)
            self.audio_player.play()
            return True
        return False
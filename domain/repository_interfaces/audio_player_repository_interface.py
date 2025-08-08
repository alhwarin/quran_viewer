#domain/repository_interfaces/audio_player_repository_interface.py
from abc import ABC, abstractmethod

class IAudioPlayer(ABC):
    @abstractmethod
    def load_playlist(self, sura_id: int, reciter: str) -> bool: pass

    @abstractmethod
    def play(self): pass

    @abstractmethod
    def pause(self): pass

    @abstractmethod
    def stop(self): pass

    @abstractmethod
    def set_volume(self, volume: int): pass


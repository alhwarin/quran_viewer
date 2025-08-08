#data/repositories/audio_player_repository_impl.py
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import QUrl
from domain.repository_interfaces.audio_player_repository_interface import IAudioPlayer
from domain.repository_interfaces.quran_repository_interface import IQuranRepository

class AudioPlayerImpl(IAudioPlayer):

    def __init__(self, quran_repository: IQuranRepository, state):
        self.quran_repository = quran_repository
        self.state = state
        self.audio_player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist.currentIndexChanged.connect(self._update_current_index)
        self.audio_player.setPlaylist(self.playlist)
        self.audio_player.setVolume(50)

    def load_playlist(self, sura_id, reciter):
        self.playlist.clear()
        audio_data = self.quran_repository.get_sura_playlist(sura_id, reciter)
        for sura_id, aya_id, path in audio_data:
            print(f"path for {sura_id}:{aya_id} → {path}")
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.playlist.setCurrentIndex(0)
        return True

    def play(self):
        self.audio_player.play()

    def pause(self):
        self.audio_player.pause()

    def resume(self):
        self.audio_player.play()

    def seek(self, value):
        self.audio_player.setPosition(value)  # FIXED: use setPosition instead of nonexistent seek()

    def stop(self):
        self.audio_player.stop()

    def duration(self):
        return self.audio_player.duration()  # FIXED: return the duration instead of just calling it

    def set_volume(self, value):
        self.audio_player.setVolume(value)

    def _update_current_index(self, index):
        """Update the current index in state when playlist changes"""
        self.state.current_aya_number = index +    1


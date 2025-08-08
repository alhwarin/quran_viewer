#presentation/events/audio_events.py
from dataclasses import dataclass
from typing import Optional
from .base_event import BaseEvent

class AudioEvent(BaseEvent):
    """Base class for all audio-related events"""
    pass

@dataclass(frozen=True)
class PlayAudioEvent(AudioEvent):
    """Event to play audio from a given sura and aya"""
    sura_id: int
    aya_number: int
    reciter_key: str

@dataclass(frozen=True)
class PauseAudioEvent(AudioEvent):
    """Event to pause currently playing audio"""
    pass

@dataclass(frozen=True)
class ResumeAudioEvent(AudioEvent):
    """Event to resume paused audio"""
    pass

@dataclass(frozen=True)
class StopAudioEvent(AudioEvent):
    """Event to stop audio playback"""
    pass

@dataclass(frozen=True)
class SeekAudioEvent:
    #def __init__(self, position_percent: int):
    position_percent : int

@dataclass(frozen=True)
class LoadRecitationForPageEvent(AudioEvent):
    """Event to load audio recitation for a specific Quran page"""
    page_number: int
    reciter_id: Optional[int] = None

@dataclass(frozen=True)
class SetVolumeEvent(AudioEvent):
    """Event to adjust playback volume"""
    volume: int  # Should be between 0 and 100

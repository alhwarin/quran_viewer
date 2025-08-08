# presentation/events/quran_events.py
from dataclasses import dataclass
from typing import Optional
from .base_event import BaseEvent
from domain.entities.page_entity import PageEntity

class QuranEvent(BaseEvent):
    """Base class for all Quran-related events"""
    pass

@dataclass(frozen=True)
class LoadFirstPageOfSuraEvent(QuranEvent):
    """Event to load the first page of a specific sura"""
    sura_id: int

@dataclass(frozen=True)
class PageNavigationEvent(QuranEvent):
    """Base class for page navigation events"""
    current_page: int

@dataclass(frozen=True)
class LoadPageEvent(QuranEvent):
    """Event to load a specific page by number"""
    page_id: int

@dataclass(frozen=True)
class LoadNextPageEvent(PageNavigationEvent):
    """Event to load the next page"""
    pass

@dataclass(frozen=True)
class LoadPreviousPageEvent(PageNavigationEvent):
    """Event to load the previous page"""
    pass

@dataclass(frozen=True)
class SuraListRequestEvent(QuranEvent):
    """Event to request the list of suras"""
    include_metadata: bool = False
    language: Optional[str] = None

@dataclass(frozen=True)
class ReciterListRequestEvent(QuranEvent):
    """Event to request the list of reciters"""
    include_details: bool = False
    audio_format: Optional[str] = None

@dataclass(frozen=True)
class PageListRequestEvent(QuranEvent):
    """Event to request the list of pages"""
    include_details: bool = False
    audio_format: Optional[str] = None



@dataclass(frozen=True)
class HighlightAyaEvent(QuranEvent):
    """Event to highlight a aya by number"""
    aya_id: int
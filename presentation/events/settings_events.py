# presentation/events/settings_events.py
from PyQt5.QtGui import QColor
from .base_event import BaseEvent

class FontSizeChangedEvent(BaseEvent):
    def __init__(self, font_size: int):
        self.font_size = font_size

class FontColorChangedEvent(BaseEvent):
    def __init__(self, color: QColor):
        self.color = color

class BackgroundColorChangedEvent(BaseEvent):
    def __init__(self, color: QColor):
        self.color = color

class HighlightColorChangedEvent(BaseEvent):
    def __init__(self, color: QColor):
        self.color = color

#presentation/events/event_dispatcher.py
from PyQt5.QtCore import QObject, pyqtSignal
from presentation.events.base_event import BaseEvent

class QuranEventDispatcher(QObject):
    event_emitted = pyqtSignal(BaseEvent)

    def __init__(self):
        super().__init__()

    def emit_event(self, event: BaseEvent):
        print(f"[Dispatcher] Emitting: {event}")
        self.event_emitted.emit(event)

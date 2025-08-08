#presentation/states/state_manager.py
from typing import Dict, Set
from presentation.states.observers import StateObserver

class StateManager:
    _observers: Dict[str, Set[StateObserver]] = {}

    @classmethod
    def add_observer(cls, source: str, observer: StateObserver):
        cls._observers.setdefault(source, set()).add(observer)

    @classmethod
    def remove_observer(cls, source: str, observer: StateObserver):
        if source in cls._observers:
            cls._observers[source].discard(observer)

    @classmethod
    def notify(cls, source: str, property_name: str):
        for observer in cls._observers.get(source, []):
            try:
                observer.on_state_changed(source, property_name)
            except Exception as e:
                print(f"[StateManager] Error notifying {observer}: {e}")

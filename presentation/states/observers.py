#presentation/states/observers.py
from abc import ABC, abstractmethod

class StateObserver(ABC):
    @abstractmethod
    def on_state_changed(self, changed_property: str):
        pass
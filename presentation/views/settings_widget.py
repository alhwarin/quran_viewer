import json
import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox, QPushButton, QColorDialog
from PyQt5.QtGui import QColor
from typing import Type
from presentation.events.settings_events import (
    FontSizeChangedEvent,
    FontColorChangedEvent,
    BackgroundColorChangedEvent,
    HighlightColorChangedEvent
)
from PyQt5.QtCore import QTimer

SETTINGS_FILE = "../config/settings.json"

class SettingsWidget(QWidget):
    MIN_FONT_SIZE = 10
    MAX_FONT_SIZE = 72
    DEFAULT_FONT_SIZE = 50

    def __init__(self, event_dispatcher, parent=None):
        super().__init__(parent)
        self.event_dispatcher = event_dispatcher
        self.settings = self._load_settings()
        self._init_ui()

    def _load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    return {
                        "font_size": data.get("font_size", self.DEFAULT_FONT_SIZE),
                        "font_color": QColor(data.get("font_color", "#90ee90")),
                        "background_color": QColor(data.get("background_color", "#000000")),
                        "highlight_color": QColor(data.get("highlight_color", "#add8e6"))
                    }
            except Exception as e:
                print(f"Failed to load settings: {e}")
        # Defaults
        return {
            "font_size": self.DEFAULT_FONT_SIZE,
            "font_color": QColor("lightgreen"),
            "background_color": QColor("black"),
            "highlight_color": QColor("lightblue")
        }

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({
                    "font_size": self.settings["font_size"],
                    "font_color": self.settings["font_color"].name(),
                    "background_color": self.settings["background_color"].name(),
                    "highlight_color": self.settings["highlight_color"].name()
                }, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Font size control
        font_size_label = QLabel("Font Size:")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(self.MIN_FONT_SIZE, self.MAX_FONT_SIZE)
        self.font_size_spin.setValue(self.settings["font_size"])
        self.font_size_spin.valueChanged.connect(self._on_font_size_changed)
        layout.addWidget(font_size_label)
        layout.addWidget(self.font_size_spin)

        # Color buttons
        self._add_color_button("Font", "font_color", FontColorChangedEvent, layout)
        self._add_color_button("Background", "background_color", BackgroundColorChangedEvent, layout)
        self._add_color_button("Highlight", "highlight_color", HighlightColorChangedEvent, layout)

        self.setLayout(layout)

        # Dispatch initial settings
        QTimer.singleShot(0, self._emit_initial_settings)

    def _emit_initial_settings(self):
        self.event_dispatcher.emit_event(FontSizeChangedEvent(font_size=self.settings["font_size"]))
        self.event_dispatcher.emit_event(FontColorChangedEvent(color=self.settings["font_color"]))
        self.event_dispatcher.emit_event(BackgroundColorChangedEvent(color=self.settings["background_color"]))
        self.event_dispatcher.emit_event(HighlightColorChangedEvent(color=self.settings["highlight_color"]))

    def _on_font_size_changed(self, value: int):
        self.settings["font_size"] = value
        self._save_settings()
        self.event_dispatcher.emit_event(FontSizeChangedEvent(value))

    def _add_color_button(self, label: str, setting_key: str, event_cls: Type, layout: QHBoxLayout):
        button = QPushButton(label)
        current_color = self.settings[setting_key]
        button.clicked.connect(lambda _, key=setting_key, e=event_cls: self._choose_and_emit_color(key, e))
        layout.addWidget(button)

    def _choose_and_emit_color(self, setting_key: str, event_class: Type):
        current_color = self.settings[setting_key]
        color = QColorDialog.getColor(current_color, self)
        if color.isValid():
            self.settings[setting_key] = color
            self._save_settings()
            self.event_dispatcher.emit_event(event_class(color))

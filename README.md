# Quran Viewer

A clean architecture-based Quran viewer with audio playback and customizable display.

## 🧱 Structure
```
quran_viewer/
├── domain/
│   ├── entities/
│   └── use_cases/
├── interfaces/
├── infrastructure/
│   └── services/
├── gui/
├── tests/
├── config/
├── main.py
├── pyproject.toml
```

## 🚀 Features
- Play aya audio by sura and reciter
- Adjust font size, background, text, and highlight colors
- Scrollable WebView highlighting current aya
- Based on PyQt5

## 🧪 Tests
```bash
pytest tests/
```

## ▶️ Run
```bash
python main.py
```

## 📦 Install
```bash
pip install .
```

---

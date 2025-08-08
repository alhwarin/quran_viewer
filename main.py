import sys
from PyQt5.QtCore import Qt, QCoreApplication

# ✅ Required for QWebEngineView to avoid ImportError
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Now safe to import PyQt5 modules
from PyQt5.QtWidgets import QApplication
from dependency_injection.container import ServiceContainer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Instantiate your DI container and launch GUI
    container = ServiceContainer()
    gui = container.get_gui()
    gui.show()

    sys.exit(app.exec_())

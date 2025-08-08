from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class WebBridge(QObject):
    # Define signals
    previous_page_requested = pyqtSignal()
    next_page_requested = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent_widget = parent
        # Connect signals to parent methods
        self.previous_page_requested.connect(parent.requestPreviousPage)
        self.next_page_requested.connect(parent.requestNextPage)

    @pyqtSlot()
    def requestPreviousPage(self):
        """Called from JavaScript when wheel scroll up at top."""
        self.previous_page_requested.emit()

    @pyqtSlot()
    def requestNextPage(self):
        """Called from JavaScript when wheel scroll down at bottom."""
        self.next_page_requested.emit()
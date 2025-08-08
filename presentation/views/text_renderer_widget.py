from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QDateTime
from presentation.web_bridge import WebBridge
from presentation.events.quran_events import (
    LoadNextPageEvent,
    LoadPreviousPageEvent,
)
from presentation.states.quran_state import QuranState
from presentation.states.state_manager import StateManager 

class TextRendererWidget(QWebEngineView):
    """A custom QWebEngineView with wheel-based page navigation."""
    

    def __init__(self, quran_state: QuranState, event_dispatcher, parent=None):
        super().__init__(parent)
        self.quran_state = quran_state
        self.event_dispatcher = event_dispatcher
        
        self._setup_web_channel()
        self.loadFinished.connect(self._on_load_finished)
        
        self._last_emit_time = QDateTime.currentMSecsSinceEpoch()
        self._scroll_debounce_time = 500  # ms to wait between emits
        StateManager.add_observer("quran", self) 

    def _setup_web_channel(self):
        """Initialize the QWebChannel and register the bridge object."""
        self.web_bridge = WebBridge(self)
        self.channel = QWebChannel(self)
        self.channel.registerObject('bridge', self.web_bridge)
        self.page().setWebChannel(self.channel)

    def _on_load_finished(self, ok: bool):
        """Handle page load completion."""
        if not ok:
            return
            
        # Initialize web channel and inject wheel event handler
        js = """
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.bridge = channel.objects.bridge;
        });

        function handleWheelEvent(e) {
            const scrollTop = Math.max(
                document.documentElement.scrollTop, 
                document.body.scrollTop
            );
            const scrollHeight = Math.max(
                document.documentElement.scrollHeight,
                document.body.scrollHeight
            );
            const clientHeight = Math.max(
                document.documentElement.clientHeight,
                document.body.clientHeight
            );
            const maxScrollTop = scrollHeight - clientHeight;
            
            // At top and scrolling up
            if (scrollTop <= 0 && e.deltaY < 0) {
                window.bridge.requestPreviousPage();
                e.preventDefault();
                return false;
            }
            // At bottom and scrolling down
            else if (scrollTop >= maxScrollTop && e.deltaY > 0) {
                window.bridge.requestNextPage();
                e.preventDefault();
                return false;
            }
        }

        document.addEventListener('wheel', handleWheelEvent, { passive: false });
        """
        
        self.page().runJavaScript(js)

    @pyqtSlot()
    def requestPreviousPage(self):
        """Handle previous page request from JavaScript."""
        current_time = QDateTime.currentMSecsSinceEpoch()
        if (current_time - self._last_emit_time) > self._scroll_debounce_time:
            self.event_dispatcher.emit_event(LoadPreviousPageEvent(self.quran_state.current_page))
            self._last_emit_time = current_time

    @pyqtSlot()
    def requestNextPage(self):
        """Handle next page request from JavaScript."""
        current_time = QDateTime.currentMSecsSinceEpoch()
        if (current_time - self._last_emit_time) > self._scroll_debounce_time:
            self.event_dispatcher.emit_event(LoadNextPageEvent(self.quran_state.current_page))
            self._last_emit_time = current_time

    def cleanup(self):
        """Clean up resources."""
        self.loadFinished.disconnect()



    def on_state_changed(self, source: str, changed_property: str):
        print(f"[STATE] {source} changed: {changed_property}")

        if source != "quran":
            return

        if changed_property == 'html_text':
            html = self.quran_state.html_text
            self.setHtml(html)
        elif changed_property == 'js_script':
            script = self.quran_state.js_script
            self.execute_js(script)
           
            
       
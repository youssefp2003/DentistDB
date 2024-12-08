import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import threading
from app import app

# Enable DPI awareness for Windows
if os.name == 'nt':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass  # Older Windows versions might not support this

class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DentisteDB Desktop")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create web view widget
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)
        
        # Start Flask server in a separate thread
        self.flask_thread = threading.Thread(target=self._run_flask)
        self.flask_thread.daemon = True
        self.flask_thread.start()
        
        # Load the Flask app URL with error handling
        try:
            self.web_view.setUrl(QUrl("http://127.0.0.1:5000"))
            self.web_view.loadFinished.connect(self._on_load_finished)
        except Exception as e:
            self._show_error("Failed to load application", str(e))
    
    def _run_flask(self):
        try:
            app.run(port=5000)
        except Exception as e:
            self._show_error("Server Error", str(e))
    
    def _on_load_finished(self, ok):
        if not ok:
            self._show_error("Load Error", "Failed to load the application interface")
    
    def _show_error(self, title, message):
        QMessageBox.critical(self, title, message)
    
    def closeEvent(self, event):
        # Cleanup when closing the application
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is not None:
                func()
        except:
            pass
        event.accept()

def main():
    # Enable Windows visual styles
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    
    # Set up Qt application with Windows-specific settings
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    qt_app = QApplication(sys.argv)
    
    try:
        window = DesktopApp()
        window.show()
        sys.exit(qt_app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Application Error", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Make sure PyQtWebEngine is installed
from PyQt5.QtCore import QUrl

# Function to start Flask app
def start_flask_app():
    os.system("python app.py")  # Adjust the command if needed (use "python3" on macOS/Linux)

# Create the main window
class PrivateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Maya - Private Window")
        self.setGeometry(100, 100, 800, 600)

        # Create a layout
        layout = QVBoxLayout()

        # Create a web view widget
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("http://localhost:5000"))  # Load the Flask app URL

        # Add the web view to the layout
        layout.addWidget(self.web_view)

        # Set the layout to a central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

# Main function
if __name__ == "__main__":
    # Start the Flask app in the background
    from threading import Thread
    flask_thread = Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Create the PyQt application
    app = QApplication(sys.argv)
    window = PrivateWindow()
    window.show()
    sys.exit(app.exec_())

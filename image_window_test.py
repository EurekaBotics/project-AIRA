import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget, QTextBrowser
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QTextCursor
from PyQt5.QtCore import Qt, QTimer

class FullScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Glassmorphism Box in Center")
        self.setGeometry(0, 0, 1920, 1080)

        background_image = QPixmap("background.png")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout to center the glass box
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the layout horizontally and vertically
        central_widget.setLayout(layout)

        self.glass_box = QFrame()
        self.glass_box.setAutoFillBackground(True)
        self.glass_box.setFrameShape(QFrame.StyledPanel)
        self.glass_box.setFrameShadow(QFrame.Sunken)
        self.glass_box.setStyleSheet("background-color: rgba(0, 0, 0, 0); border-radius: 20px")  # Transparent initially

        # Set a fixed size for the glass box (e.g., 1700x900)
        self.glass_box.setFixedSize(1700, 900)

        # Initially hide the glass box
        self.glass_box.hide()

        layout.addWidget(self.glass_box)

        # Create a QTextBrowser widget for displaying text with custom font
        self.text_browser = QTextBrowser(self.glass_box)
        self.text_browser.setOpenExternalLinks(True)  # Enable clickable links
        self.text_browser.setOpenLinks(True)
        self.text_browser.setReadOnly(True)  # Make it read-only to prevent text editing
        self.text_browser.setGeometry(100, 100, 1500, 600)  # Adjust the geometry to fit your layout
        self.text_browser.setStyleSheet("color: white; background: transparent;")  # Set text color to white and background transparent

        # Hide the scrollbar
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set custom font size and font family
        font = QFont()
        font.setPointSize(65)  # Adjust the font size as needed
        font.setFamily("Arial")  # Adjust the font family as needed
        self.text_browser.setFont(font)

        # Initialize the text buffer
        self.text_buffer = []

        # Schedule the appearance of the glass box with a custom fade-in effect after 2 seconds
        QTimer.singleShot(2000, self.fadeIn)

        # Simulate text coming to the buffer in a loop
        self.text_to_simulate = [
    "This is text 1.",
    "Here comes text 2.",
    "Text 3 is here.",
    "And now text 4 arrives.",
    "Fifth text entry.",
    "Sixth text entry.",
    "Seventh text entry.",
    "Eighth text entry.",
    "Ninth text entry.",
    "Tenth text entry.",
    "Eleventh text entry.",
    "Twelfth text entry.",
    "Thirteenth text entry.",
    "Fourteenth text entry.",
    "Fifteenth text entry.",
    "Sixteenth text entry.",
    "Seventeenth text entry.",
    "Eighteenth text entry.",
    "Nineteenth text entry.",
    "Twentieth text entry."
]

        self.simulation_index = 0

        # Start the text simulation
        self.simulateText()

    def fadeIn(self):
        self.glass_box.show()
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.upOpacity)
        self.fade_timer.start(30)  # Adjust the timer interval for smoother fading
        self.fade_target_opacity = 0.8
        self.fade_current_opacity = 0.0

    def upOpacity(self):
        self.fade_current_opacity += 0.1  # Adjust the step size for smoother fading
        self.glass_box.setStyleSheet(f"background-color: rgba(0, 0, 0, {self.fade_current_opacity}); border-radius: 20px")
        if self.fade_current_opacity >= self.fade_target_opacity:
            self.fade_timer.stop()

    def downOpacity(self):
        self.fade_current_opacity -= 0.1  # Adjust the step size for smoother fading
        self.glass_box.setStyleSheet(f"background-color: rgba(0, 0, 0, {self.fade_current_opacity}); border-radius: 20px")
        if self.fade_current_opacity <= self.fade_target_opacity:
            self.fade_timer.stop()

    def fadeOut(self):
        self.text_buffer.clear()  # Clear the text buffer
        self.text_browser.clear()  # Clear the text in the QTextBrowser
        self.glass_box.hide()

    def updateText(self):
        self.text_browser.clear()  # Clear the text in the QTextBrowser
        self.text_browser.setPlainText("\n".join(self.text_buffer))  # Set the text from the buffer
        self.text_browser.moveCursor(QTextCursor.End)

    def addText(self, text):
        self.text_buffer.append(text)  # Add text to the buffer
        self.updateText()  # Update the displayed text

    def simulateText(self):
        if self.simulation_index < len(self.text_to_simulate):
            self.addText(self.text_to_simulate[self.simulation_index])
            self.simulation_index += 1
            QTimer.singleShot(1000, self.simulateText)  # Add text every 3 seconds

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenApp()
    window.showFullScreen()

    sys.exit(app.exec_())

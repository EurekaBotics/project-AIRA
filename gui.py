import sys
import time
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTextBrowser,
    QGraphicsOpacityEffect,
    QPushButton,
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QTextCursor, QColor
from PyQt5.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QThread,
    pyqtSignal,
)


class TextSimulationThread(QThread):
    text_generated = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TextSimulationThread, self).__init__(parent)
        self.text_to_simulate = ["I'm all ears"]

    def set_text_to_simulate(self, new_text):
        self.text_to_simulate.append(new_text)

    def remove_text(self):
        if self.text_to_simulate:
            self.text_to_simulate.pop(0)

    def run(self):
        self.msleep(2000)
        while True:
            if not len(self.text_to_simulate):
                time.sleep(1)
                continue

            for text in self.text_to_simulate:
                self.text_generated.emit(text)
                self.msleep(1000)
                self.remove_text()


class FullScreenApp(QMainWindow):

    glassBoxVisible = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.image_path = "./Images/background.png"
        self.text_size = 35
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Glassmorphism Box in Center")
        self.setGeometry(0, 0, 1920, 1200)

        # Set focus policy to enable keyboard events
        self.setFocusPolicy(Qt.StrongFocus)

        # Set background image
        self.setBackgroundImage()

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setupLayout()

        # Create glassmorphism box
        self.setupGlassBox()

        # Create QTextBrowser widget for displaying text with custom font
        self.setupTextBrowser()

        # Create toggle button
        self.setupToggleButton()

        # Timer for the initial fade-in
        QTimer.singleShot(2000, self.fadeIn)

        # Create and start the text simulation thread
        self.text_simulation_thread = TextSimulationThread()
        self.text_simulation_thread.text_generated.connect(self.simulateText)
        self.text_simulation_thread.start()

    def setBackgroundImage(self):
        background_image = QPixmap(self.image_path)

        if background_image.isNull():
            print(f"Error: Unable to load the image from {self.image_path}")
            return

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

    def setupLayout(self):
        layout = QVBoxLayout(self.central_widget)
        layout.setAlignment(Qt.AlignCenter)

    def setupGlassBox(self):
        self.glass_box = QWidget()
        self.glass_box.setGraphicsEffect(QGraphicsOpacityEffect())
        self.glass_box.setAutoFillBackground(True)

        # Set the background color to black with transparency and rounded edges
        black_color = QColor(0, 0, 0)
        black_color.setAlphaF(
            0.7
        )  # Adjust the alpha value for the desired transparency
        self.glass_box.setStyleSheet(
            f"background-color: {black_color.name()}; border-radius: 20px;"  # Adjust the radius as needed
        )

        self.glass_box.setFixedSize(1700, 900)
        self.glass_box.hide()

        layout = self.central_widget.layout()
        layout.addWidget(self.glass_box)

    def setupTextBrowser(self):
        self.text_browser = QTextBrowser(self.glass_box)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setOpenLinks(True)
        self.text_browser.setReadOnly(True)
        self.text_browser.setStyleSheet("color: white; background: transparent;")
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QFont()
        font.setPointSize(self.text_size)
        font.setFamily("Arial")
        self.text_browser.setFont(font)

        # Set the text browser's size to match the glass box
        self.text_browser.setFixedSize(self.glass_box.size())

    def setupToggleButton(self):
        self.toggle_button = QPushButton("Toggle Fullscreen", self.central_widget)
        self.toggle_button.setStyleSheet(
            "background: transparent; color: white; border: 1px solid white;"
        )
        self.toggle_button.clicked.connect(self.toggleFullscreen)

    def fadeIn(self):
        self.glass_box.show()
        self.opacity_animation = QPropertyAnimation(
            self.glass_box.graphicsEffect(), b"opacity"
        )
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(0.8)
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setEasingCurve(QEasingCurve.Linear)
        self.opacity_animation.finished.connect(
            self.glassBoxVisible.emit
        )  # Emit the signal when the animation is complete
        self.opacity_animation.start()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Toggle between fullscreen and normal mode
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def toggleFullscreen(self):
        # Toggle between fullscreen and normal mode
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def fadeOut(self):
        self.text_buffer.clear()
        self.text_browser.clear()
        self.glass_box.hide()

    def updateText(self):
        self.text_browser.clear()
        self.text_browser.setPlainText("\n".join(self.text_buffer))
        self.text_browser.moveCursor(QTextCursor.End)

    def addText(self, text):
        self.text_browser.append(text)
        self.text_browser.moveCursor(QTextCursor.End)

    def simulateText(self, text):
        # Check if the glass box is visible before adding text
        if self.glass_box.isVisible():
            self.addText(text)
        else:
            # Connect the signal to the simulateText method to handle the case when the glass box becomes visible
            self.glassBoxVisible.connect(lambda: self.simulateText(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullScreenApp()
    window.showFullScreen()
    sys.exit(app.exec_())

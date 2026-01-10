from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QStackedWidget,
)
from scenes import (
    welcome_scene,
    home_scene,
    warnings_scene,
    detailed_scene,
)
from config import ConfigurationClass
    
class MainApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.resize(self.config.window_width,self.config.window_width//2)
        self.setWindowTitle("Weather Application")

        self.scenes = QStackedWidget()
        self.scenes.addWidget(welcome_scene.Scene())
        self.scenes.setCurrentIndex(0)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.scenes)

        self.setLayout(self.main_layout)

app = QApplication([])

main_window = MainApplication()

main_window.show()
app.exec()
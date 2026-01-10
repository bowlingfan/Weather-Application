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

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()
    """
    Creating/Setup QT Window
    """
    def create_widgets(self):
        self.scenes = QStackedWidget()
        self.welcome_scene = welcome_scene.Scene()
        self.home_scene = home_scene.Scene()

    def design_widgets(self):
        pass

    def design_layouts(self):
        self.scenes.addWidget(self.welcome_scene)
        self.scenes.addWidget(self.home_scene)
        self.scenes.setCurrentIndex(1)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.scenes)

        self.setLayout(self.main_layout)

    def connect_events(self):
        self.welcome_scene.confirm_button.clicked.connect(self.welcome_confirm_button_clicked)
    """
    Cross-scene events:
        Events that occur within another scene that require changes to MainApplication QWidget.
    """
    def welcome_confirm_button_clicked(self):
        location_text = self.welcome_scene.location_text_box.text()
        if location_text == "":
            self.welcome_scene.guide.setText("Provide a location before pressing confirm.")
            return
        """
        self.config.get_API_data > (error_code [0], msg [1])
        """
        result = self.config.get_API_data(location_text)
        if result[0] != 0:
            self.welcome_scene.guide.setText(result[1])
        else:
            self.request_change_scene("detailed_scene")
    """
    Utility functions 
    """
    def request_change_scene(self, new_scene):
        if new_scene not in self.config.scenes_available:
            raise BaseException("SCENE NOT VALID")
        print("change")
        self.scenes.setCurrentIndex(self.config.scenes_available[new_scene])

app = QApplication([])

main_window = MainApplication()

main_window.show()
app.exec()
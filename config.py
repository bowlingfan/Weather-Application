from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase

"""
PRIVATE VARIABLES
"""
default_font_directory = "resource/Roboto-Light.ttf"
class WelcomeConfig():
    def __init__(self):
        self.user_action_textbox_size = QSize(300,35)
        self.user_action_button_size = QSize(100,35)
class ConfigurationClass():
    def __init__(self):
        self.window_width=700

        self.default_font_size = 15
        self.default_font_small_size = 8

        self.default_font = self.make_font(self.default_font_size)
        self.default_font_small = self.make_font(self.default_font_small_size)

        self.welcome_config = WelcomeConfig()
    def make_default_QFont(self):
        """
        Returns QFont object with default settings.
        """
        qid = QFontDatabase.addApplicationFont(default_font_directory)
        # There is only 1 child font of the given Font Family.
        return QFont(QFontDatabase.applicationFontFamilies(qid)[0])

    def make_font(self, fontSize : int):
        font = self.make_default_QFont()
        font.setPointSize(fontSize)
        return font
    
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

from setup_window import SetupWindow
from teleop_window import TeleopWindow
from record_replay_window import RecordReplayWindow
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,

    EN,
    DE,

    TELEOP,
    RECORD_REPLAY,

    SETUP_WINDOW,
    TELEOP_WINDOW,
    RECORD_REPLAY_WINDOW,

    LOGO_HTWK_FILE,
    SETUP_BUTTON_ORANGE_FILE,
    SETUP_BUTTON_BLACK_FILE
)





class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # general settings
        self.setWindowTitle("SO Arm UI")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white;")

        # set inital language to English
        self.language = EN

        # set initial window to setup
        self.actual_window = SETUP_WINDOW

        # main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # top layout
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(10, 8, 10, 2)
        self.top_layout.setSpacing(3)

        # HTWK logo
        self.logo_htwk = QLabel()
        self.logo_htwk.setPixmap(
            QPixmap((LOGO_HTWK_FILE)).scaled(
                65, 65,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        self.top_layout.addWidget(self.logo_htwk)

        # add horizontal space
        self.top_layout.addStretch()

        # style for tab buttons
        self.TAB_STYLE = """
        QPushButton {
            background-color: #000000;
            color: #ffffff;
            border: 1px solid #000000;
            border-radius: 8px;
            padding: 6px 14px;
            font-weight: bold;
            font-size: 12px;
            padding-top: 1px;
            padding-bottom: 1px;
        }

        QPushButton:checked {
            background-color: #ff8c00;
            color: #000000;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            padding-left: 1px;
            padding-right: 1px;
        }
        """

        # style for language buttons
        self.LANGUAGE_STYLE = """
        QPushButton {
            background-color: #000000;
            color: #ffffff;
            border: 1px solid #000000;
            padding: 4px 6px;
            min-width: 0px;
            min-height: 0px;
            font-size: 12px;
            font-weight: bold;
        }

        QPushButton:checked {
            background-color: #ff8c00;
            color: #000000;
            min-width: 0px;
            min-height: 0px;
            font-size: 14px;
            font-weight: bold;
        }
        """

        # set push buttons
        self.setup_button = QPushButton()
        self.teleop_button = QPushButton(TELEOP)
        self.record_replay_button = QPushButton(RECORD_REPLAY)

        # set toggle buttons for (only "ON/OFF")
        self.setup_button.setCheckable(True)
        self.teleop_button.setCheckable(True)
        self.record_replay_button.setCheckable(True)

        # activate setup button in initial state
        self.setup_button.setChecked(True)

        # set stylesheet for setup icon (orange as active in initial state)
        self.setup_button.setIcon(QIcon(SETUP_BUTTON_ORANGE_FILE))
        self.setup_button.setIconSize(QSize(30, 30))
        self.setup_button.setStyleSheet("border: none;")

        # fixed hight for buttons
        self.teleop_button.setFixedHeight(30)
        self.record_replay_button.setFixedHeight(30)

        # set stylesheet for teleop/record&replay tabs
        self.teleop_button.setStyleSheet(self.TAB_STYLE)
        self.record_replay_button.setStyleSheet(self.TAB_STYLE)

        # add buttons to layout
        self.top_layout.addWidget(self.setup_button)
        self.top_layout.addWidget(self.teleop_button)
        self.top_layout.addWidget(self.record_replay_button)

        # set language buttons
        self.german_button = QPushButton(DE)
        self.english_button = QPushButton(EN)

        # set to toggle buttons (only "ON/OFF")
        self.german_button.setCheckable(True)
        self.english_button.setCheckable(True)

        # set stylesheet
        self.german_button.setStyleSheet(self.LANGUAGE_STYLE)
        self.english_button.setStyleSheet(self.LANGUAGE_STYLE)

        # set initial language to EN
        self.english_button.setChecked(True)

        # add horizontal space
        self.top_layout.addStretch()

        # add language buttons to layout
        self.top_layout.addWidget(self.german_button)
        self.top_layout.addWidget(self.english_button)

        # set layout
        self.layout.addLayout(self.top_layout)

        # set widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # initialize stack
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # add tabs
        self.setup_view = SetupWindow(self.language)
        self.teleop_view = TeleopWindow(self.language)
        self.record_view = RecordReplayWindow(self.language)

        # add widgets
        self.stack.addWidget(self.setup_view)
        self.stack.addWidget(self.teleop_view)
        self.stack.addWidget(self.record_view)

        # set initial view to setup
        self.switch_view(0)

        # set connections for buttons
        self.setup_button.clicked.connect(self.show_setup)
        self.teleop_button.clicked.connect(self.show_teleop)
        self.record_replay_button.clicked.connect(self.show_record_replay)

        # set language
        self.english_button.clicked.connect(self.set_english)
        self.german_button.clicked.connect(self.set_german)



    def switch_view(self, view_index):

        # get current index
        self.stack.setCurrentIndex(view_index)

        # update button states
        self.setup_button.setChecked(view_index == 0)
        self.teleop_button.setChecked(view_index == 1)
        self.record_replay_button.setChecked(view_index == 2)

        # update settings icon (orange in setup window, otherwise black)
        if view_index == 0:
            self.setup_button.setIcon(QIcon(SETUP_BUTTON_ORANGE_FILE))
        else:
            self.setup_button.setIcon(QIcon(SETUP_BUTTON_BLACK_FILE))



    def show_setup(self):

        if self.actual_window == SETUP_WINDOW:
            self.setup_button.setChecked(True)
            return
        
        if self.actual_window == TELEOP_WINDOW:
            self.teleop_view.stop()

        elif self.actual_window == RECORD_REPLAY_WINDOW:
            self.record_view.stop()

        self.switch_view(SETUP_WINDOW)

        self.setup_view.start()

        self.actual_window = SETUP_WINDOW
        
        self.setup_button.setChecked(True)
        self.teleop_button.setChecked(False)
        self.record_replay_button.setChecked(False)



    def show_teleop(self):
        
        if self.actual_window == TELEOP_WINDOW:
            self.teleop_button.setChecked(True)
            return

        if self.actual_window == SETUP_WINDOW:
            self.setup_view.stop()

        elif self.actual_window == RECORD_REPLAY_WINDOW:
            self.record_view.stop()

        self.switch_view(TELEOP_WINDOW)

        self.actual_window = TELEOP_WINDOW
        
        self.setup_button.setChecked(False)
        self.teleop_button.setChecked(True)
        self.record_replay_button.setChecked(False)



    def show_record_replay(self):

        if self.actual_window == RECORD_REPLAY_WINDOW:
            self.record_replay_button.setChecked(True)
            return

        if self.actual_window == SETUP_WINDOW:
            self.setup_view.stop()
        
        elif self.actual_window == TELEOP_WINDOW:
            self.teleop_view.stop()
        
        self.switch_view(RECORD_REPLAY_WINDOW)

        self.actual_window = RECORD_REPLAY_WINDOW

        self.setup_button.setChecked(False)
        self.teleop_button.setChecked(False)
        self.record_replay_button.setChecked(True)



    def set_english(self):

        if self.language == EN:
            self.english_button.setChecked(True)
            return
        
        self.language = EN
        self.english_button.setChecked(True)
        self.german_button.setChecked(False)

        if self.actual_window == SETUP_WINDOW:
            self.setup_view.set_english()
        else:
            self.setup_view.update_language(EN)

        self.teleop_view.set_english()
        self.record_view.set_english()


    def set_german(self):

        if self.language == DE:
            self.german_button.setChecked(True)
            return
        
        self.language = DE
        self.english_button.setChecked(False)
        self.german_button.setChecked(True)

        if self.actual_window == SETUP_WINDOW:
            self.setup_view.set_german()
        else:
            self.setup_view.update_language(DE)

        self.teleop_view.set_german()
        self.record_view.set_german()

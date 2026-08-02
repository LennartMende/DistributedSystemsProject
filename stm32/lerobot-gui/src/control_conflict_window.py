import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel
from PyQt5.QtCore import Qt
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

app = QApplication(sys.argv)

if sys.argv[1] == "control":
    window = QLabel("You can control the follower arm by moving the sliders.")
elif sys.argv[1] == "conflict":
    window = QLabel("There is a conflict caused by the opened browser windows.\n" \
    "You have to follow those rules:\n" \
    "1. You can't have a Control tab open at the same time as an Index or Diagram tab.\n" \
    "2. You can't have multiple control windows opened at the same time.")
else:
    raise ValueError 

window.setAlignment(Qt.AlignCenter)

window.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.setWordWrap(True)
window.setStyleSheet("""
    QLabel {
        background-color: #fff;
        color: #111;
        font-family: monospace;
        font-size: 20px;
        border: none;
    }
""")

window.showFullScreen()

app.exec()

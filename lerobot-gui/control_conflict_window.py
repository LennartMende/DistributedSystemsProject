import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel

app = QApplication(sys.argv)

if sys.argv[1] == "control":
    window = QLabel("You can control the follower arm by moving the sliders.")
elif sys.argv[1] == "conflict":
    window = QLabel("There is a conflict because of the opened browser windows:\n" \
    "You have to follow those rules:\n" \
    "1. You can't have an (index tab || diagram tab) && control tab open at the same time.\n" \
    "2. You can't have multiple control windows opened at the same time.")
else:
    raise ValueError 

window.show()

app.exec()

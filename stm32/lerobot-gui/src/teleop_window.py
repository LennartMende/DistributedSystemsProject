from dataclasses import dataclass
import time

from PyQt5.QtCore import Qt, QSize, QProcess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon

from lerobot.utils import ClientCfg, publish
from lerobot.utils import connect as connect_client

from constants import (
    EN, DE,

    IDLE, READY, TELEOPERATING, CONNECTING, RESETTING,

    WELCOME_TEXT_EN, WELCOME_TEXT_DE,

    START_BUTTON_ICON_FILE,
    STOP_BUTTON_ICON_FILE,

    TELEOPERATION_START_INSTRUCTION_EN,
    TELEOPERATION_START_INSTRUCTION_DE,
    TELEOPERATION_STOP_INSTRUCTION_EN,
    TELEOPERATION_STOP_INSTRUCTION_DE,
    TELEOPERATION_STARTED_EN,
    TELEOPERATION_STARTED_DE,
    TELEOPERATION_STOPPED_EN,
    TELEOPERATION_STOPPED_DE,

    RESETTING_STATUS_TELEOP_EN,
    RESETTING_STATUS_TELEOP_DE,
    RESETTING_STOP_INSTRUCTION_EN,
    RESETTING_STOP_INSTRUCTION_DE,

    CONNECTION_STATUS_EN,
    CONNECTION_STATUS_DE,
    CONNECTION_STOP_INSTRUCTION_EN,
    CONNECTION_STOP_INSTRUCTION_DE,
    CONNECTION_FINISHED_TEXT_EN,
    CONNECTION_FINISHED_TEXT_DE,

    TELEOPERATING_STATUS_EN,
    TELEOPERATING_STATUS_DE,
    READY_STATUS_EN,
    READY_STATUS_DE,
    IDLE_STATUS_EN,
    IDLE_STATUS_DE,

    TELEOP_COMMAND
)


# state
# system_state_topic = "system/state"
# client_id = 'system_state_publisher'
# clientCfg = ClientCfg(client_id=client_id)


class TeleopWindow(QWidget):

    def __init__(self, language):
        super().__init__()

        # general settings
        self.process = QProcess(self)
        self.state = IDLE 
        self.already_started = False

        # initialize language
        self.language = language

        # initialize empty page layout - not self.layout because it would overwrite layout from MainWindow!
        layout = QVBoxLayout()

        # last action
        self.last_action = QLabel(WELCOME_TEXT_EN)
        self.last_action.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.last_action.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.last_action)

        # instruction
        self.instruction = QLabel(TELEOPERATION_START_INSTRUCTION_EN)
        self.instruction.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction)

        # start button
        self.start_button = QPushButton("")
        self.start_button.setStyleSheet("font-size: 20px; font-weight: bold; border: none;")
        self.start_button.setIcon(QIcon(START_BUTTON_ICON_FILE))
        self.start_button.setIconSize(QSize(130, 130))
        layout.addWidget(self.start_button)
        
        # stop button
        self.stop_button = QPushButton("")
        self.stop_button.setStyleSheet("font-size: 20px; font-weight: bold; border: none;")
        self.stop_button.setIcon(QIcon(STOP_BUTTON_ICON_FILE))
        self.stop_button.setIconSize(QSize(130, 130))
        self.stop_button.hide()
        layout.addWidget(self.stop_button)

        # status text
        self.status = QLabel(IDLE_STATUS_EN)
        layout.addWidget(self.status)
        self.status.setStyleSheet("font-size: 20px; font-weight: bold; font-style: italic;")
        self.status.setAlignment(Qt.AlignCenter)

        # actions on clicks
        self.start_button.clicked.connect(self.run)
        self.stop_button.clicked.connect(self.stop)

        # set layout
        self.setLayout(layout)
        
        #create a publisher for state messages
        # self.system_state_publisher = connect_client(clientCfg=clientCfg)
        self.start_time = time.perf_counter()


    def run(self) -> None:

        self.already_started = True
        self.state = CONNECTING
        self.start_button.hide()
        self.stop_button.show()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.start(TELEOP_COMMAND[0], TELEOP_COMMAND[1:])

        if self.language == EN:
            self.setText(TeleopWindow.TextCfg(TELEOPERATION_STARTED_EN, CONNECTION_STOP_INSTRUCTION_EN, CONNECTION_STATUS_EN))
        else:
            self.setText(TeleopWindow.TextCfg(TELEOPERATION_STARTED_DE, CONNECTION_STOP_INSTRUCTION_DE, CONNECTION_STATUS_DE))

        # publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "TELEOPERATING"}, start_time=self.start_time)


    def stop(self) -> None:

        self.state = (READY if self.already_started else IDLE)
        self.stop_button.hide()
        self.start_button.show()

        if self.process:
            self.process.terminate()
            self.process = None
        
        if self.state == READY:
            if self.language == EN:
                self.setText(TeleopWindow.TextCfg(TELEOPERATION_STOPPED_EN, TELEOPERATION_START_INSTRUCTION_EN, READY_STATUS_EN))
            else:
                self.setText(TeleopWindow.TextCfg(TELEOPERATION_STOPPED_DE, TELEOPERATION_START_INSTRUCTION_DE, READY_STATUS_DE))
        
        elif self.state == IDLE:
            if self.language == EN:
                self.setText(TeleopWindow.TextCfg(WELCOME_TEXT_EN, TELEOPERATION_START_INSTRUCTION_EN, IDLE_STATUS_EN))
                return
            else:
                self.setText(TeleopWindow.TextCfg(WELCOME_TEXT_DE, TELEOPERATION_START_INSTRUCTION_DE, IDLE_STATUS_DE))

        else:
            raise Exception("Illegal state")

        # publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "STOPPED"}, start_time=self.start_time)

    def set_english(self) -> None:

        if self.language == EN:
            return
        
        self.language = EN

        if self.state == IDLE:
            self.setText(TeleopWindow.TextCfg(WELCOME_TEXT_EN, TELEOPERATION_START_INSTRUCTION_EN, IDLE_STATUS_EN))
            return
        
        if self.state == CONNECTING:
            self.setText(TeleopWindow.TextCfg(TELEOPERATION_STARTED_EN, CONNECTION_STOP_INSTRUCTION_EN, CONNECTION_STATUS_EN))
            return
        
        if self.state == RESETTING:
            self.setText(TeleopWindow.TextCfg(CONNECTION_FINISHED_TEXT_EN, RESETTING_STOP_INSTRUCTION_EN, RESETTING_STATUS_TELEOP_EN))
            return
        
        if self.state == TELEOPERATING:
            self.setText(TeleopWindow.TextCfg(TELEOPERATION_STARTED_EN, TELEOPERATION_STOP_INSTRUCTION_EN, TELEOPERATING_STATUS_EN))
            return
        
        # otherwise automatically in READY state
        self.setText(TeleopWindow.TextCfg(TELEOPERATION_STOPPED_EN, TELEOPERATION_START_INSTRUCTION_EN, READY_STATUS_EN))
        return


    def set_german(self):

        if self.language == DE:
            return
        
        self.language = DE

        if self.state == IDLE:
            self.setText(TeleopWindow.TextCfg(WELCOME_TEXT_DE, TELEOPERATION_START_INSTRUCTION_DE, IDLE_STATUS_DE))
            return
        
        if self.state == CONNECTING:
            self.setText(TeleopWindow.TextCfg(TELEOPERATION_STARTED_DE, CONNECTION_STOP_INSTRUCTION_DE, CONNECTION_STATUS_DE))
            return
        
        if self.state == RESETTING:
            self.setText(TeleopWindow.TextCfg(CONNECTION_FINISHED_TEXT_DE, RESETTING_STOP_INSTRUCTION_DE, RESETTING_STATUS_TELEOP_DE))
            return
        
        if self.state == TELEOPERATING:
            self.setText(TeleopWindow.TextCfg(TELEOPERATION_STARTED_DE, TELEOPERATION_STOP_INSTRUCTION_DE, TELEOPERATING_STATUS_DE))
            return
        
        # otherwise automatically in READY state
        self.setText(TeleopWindow.TextCfg(TELEOPERATION_STOPPED_DE, TELEOPERATION_START_INSTRUCTION_DE, READY_STATUS_DE))
        return



    def setText(self, textCfg: "TeleopWindow.TextCfg"):
        self.last_action.setText(textCfg.last_action)
        self.instruction.setText(textCfg.instruction)
        self.status.setText(textCfg.status)


    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode()

        for line in data.splitlines():
            line = line.strip()

            if line == "CONNECTED" and self.state == CONNECTING:
                self.state = RESETTING

                # if self.language == EN:
                #     self.setText(TeleopWindow.TextCfg(
                #         "Resetting robot to rest pose...",
                #         "",
                #         "RESETTING"
                #     ))

                if self.language == EN:
                    self.setText(TeleopWindow.TextCfg(
                        CONNECTION_FINISHED_TEXT_EN , RESETTING_STOP_INSTRUCTION_EN, RESETTING_STATUS_TELEOP_EN
                    ))

                else:
                    self.setText(TeleopWindow.TextCfg(
                        CONNECTION_FINISHED_TEXT_DE , RESETTING_STOP_INSTRUCTION_DE, RESETTING_STATUS_TELEOP_DE
                    ))

            elif line == "READY" and self.state != TELEOPERATING:
                self.state = TELEOPERATING

                if self.language == EN:
                    self.setText(TeleopWindow.TextCfg(
                        TELEOPERATION_STARTED_EN,
                        TELEOPERATION_STOP_INSTRUCTION_EN,
                        TELEOPERATING_STATUS_EN
                    ))
                if self.language == DE:                                                                                             
                    self.setText(TeleopWindow.TextCfg(                                                     
                        TELEOPERATION_STARTED_DE,             
                        TELEOPERATION_STOP_INSTRUCTION_DE,
                        TELEOPERATING_STATUS_DE                                                                               
                    ))



    @dataclass
    class TextCfg:
        last_action: str
        instruction: str
        status: str


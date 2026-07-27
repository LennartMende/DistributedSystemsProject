import json
import time

from dataclasses import dataclass
from PyQt5.QtCore import Qt, QSize, QProcess
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon

from lerobot.utils import ClientCfg, publish
from lerobot.utils import connect as connect_client

from constants import (
    EN,
    DE,

    IDLE,
    READY,
    RECORDING,
    RESETTING,
    REPLAYING,
    FINISHED,

    WELCOME_TEXT_EN,
    WELCOME_TEXT_DE,

    START_BUTTON_ICON_FILE,
    STOP_BUTTON_ICON_FILE,

    RECORD_START_INSTRUCTION_EN,
    RECORD_START_INSTRUCTION_DE,
    RECORD_STOP_INSTRUCTION_EN,
    RECORD_STOP_INSTRUCTION_DE,
    RESETTING_STOP_INSTRUCTION_EN,
    RESETTING_STOP_INSTRUCTION_DE,
    REPLAY_STOP_INSTRUCTION_EN,
    REPLAY_STOP_INSTRUCTION_DE,
    RECORD_START_AGAIN_INSTRUCTION_EN,
    RECORD_START_AGAIN_INSTRUCTION_DE,

    RECORDING_STARTED_EN,
    RECORDING_STARTED_DE,
    RECORDING_STOPPED_DE,
    RECORDING_STOPPED_EN,

    NEXT_STEP_RESETTING_EN,
    NEXT_STEP_RESETTING_DE,

    RECORDING_STATUS_START_EN,
    RECORDING_STATUS_START_DE,
    RECORDING_STATUS_TEXT_EN,
    RECORDING_STATUS_TEXT_BEFORE_S_DE,
    RECORDING_STATUS_TEXT_AFTER_S_DE,

    REPLAYING_STARTED_EN,
    REPLAYING_STARTED_DE,
    REPLAYING_STATUS_TEXT_EN,
    REPLAYING_STATUS_TEXT_DE,

    RESETTING_STATUS_TEXT_EN,
    RESETTING_STATUS_TEXT_DE,

    IDLE_STATUS_EN,
    IDLE_STATUS_DE,
    FINISHED_EN,
    FINISHED_DE,
    READY_STATUS_EN,
    READY_STATUS_DE,

    SECONDS,

    RECORD_REPLAY_COMMAND
)


# state
system_state_topic = "system/state"
client_id = 'system_state_publisher'
clientCfg = ClientCfg(client_id=client_id)


class RecordReplayWindow(QWidget):

    def __init__(self, language):
        super().__init__()

        # general settings
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)
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
        self.instruction = QLabel(RECORD_START_INSTRUCTION_EN)
        self.instruction.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction)

        # start button
        self.start_button = QPushButton("")
        self.start_button.setStyleSheet("font-size: 20px; font-weight: bold; border: none;")
        self.start_button.setIcon(QIcon(START_BUTTON_ICON_FILE))
        self.start_button.setIconSize(QSize(130, 130))
        layout.addWidget(self.start_button)
        
        # Stop button
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

        # remaining counter
        self.remaining_msg: int | None = 20

        # Actions on clicks
        self.start_button.clicked.connect(self.run)
        self.stop_button.clicked.connect(self.stop)

        # set layout
        self.setLayout(layout)

        #create a publisher for state messages
        self.system_state_publisher = connect_client(clientCfg=clientCfg)
        self.start_time = time.perf_counter()

    def run(self) -> None:

        self.already_started = True
        self.state = RECORDING
        self.start_button.hide()
        self.stop_button.show()
        self.process.kill()

        cmd = RECORD_REPLAY_COMMAND                                                                                                                                                                                                                                              
        self.process.start(cmd[0], cmd[1:])
        
        if self.language == EN:
            self.setText(RecordReplayWindow.TextCfg(RECORDING_STARTED_EN, RECORD_STOP_INSTRUCTION_EN, RECORDING_STATUS_START_EN))
        else:
            self.setText(RecordReplayWindow.TextCfg(RECORDING_STARTED_DE, RECORD_STOP_INSTRUCTION_DE, RECORDING_STATUS_START_DE)) 
    
    def stop(self) -> None:

        self.state = (READY if self.already_started else IDLE)
        self.stop_button.hide()
        self.start_button.show()

        if self.process.state() != QProcess.NotRunning:
            self.process.kill()
        
        if self.state == READY:
            if self.language == EN:
                self.setText(RecordReplayWindow.TextCfg(RECORDING_STOPPED_EN, RECORD_START_INSTRUCTION_EN, READY_STATUS_EN))
            else:
                self.setText(RecordReplayWindow.TextCfg(RECORDING_STOPPED_DE, RECORD_START_INSTRUCTION_DE, READY_STATUS_DE))
        
        elif self.state == IDLE:
            if self.language == EN:
                self.setText(RecordReplayWindow.TextCfg(WELCOME_TEXT_EN, RECORD_START_INSTRUCTION_EN, IDLE_STATUS_EN))
                return
            else:
                self.setText(RecordReplayWindow.TextCfg(WELCOME_TEXT_DE, RECORD_START_INSTRUCTION_DE, IDLE_STATUS_DE))
            
        else:
            raise Exception("Illegal state")

        publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "STOPPED"}, start_time=self.start_time)

    def set_english(self) -> None:

        if self.language == EN:
            return
        
        self.language = EN

        if self.state == IDLE:
            self.setText(RecordReplayWindow.TextCfg(WELCOME_TEXT_EN, RECORD_START_INSTRUCTION_EN, IDLE_STATUS_EN))
            return
        
        elif self.state == RECORDING:
            self.setText(RecordReplayWindow.TextCfg(
                RECORDING_STARTED_EN, RECORD_STOP_INSTRUCTION_EN, RECORDING_STATUS_TEXT_EN + str(self.remaining_msg) + SECONDS
            ))
            return
        
        elif self.state == RESETTING:
            self.setText(RecordReplayWindow.TextCfg(
                NEXT_STEP_RESETTING_EN, RESETTING_STOP_INSTRUCTION_EN, RESETTING_STATUS_TEXT_EN + str(self.remaining_msg) + SECONDS
            ))
            return
        
        elif self.state == REPLAYING:
            self.setText(RecordReplayWindow.TextCfg(
                REPLAYING_STARTED_EN, REPLAY_STOP_INSTRUCTION_EN, REPLAYING_STATUS_TEXT_EN + str(self.remaining_msg) + SECONDS
                ))
            return
        
        elif self.state == FINISHED:
            self.setText(RecordReplayWindow.TextCfg(
                FINISHED_EN, RECORD_START_AGAIN_INSTRUCTION_EN, FINISHED_EN
                ))
            return
        
        # otherwise automatically in READY state
        self.setText(RecordReplayWindow.TextCfg(RECORDING_STOPPED_EN, RECORD_START_INSTRUCTION_EN, READY_STATUS_EN))
        return


    def set_german(self):

        if self.language == DE:
            return
        
        self.language = DE
        
        if self.state == IDLE:
            self.setText(RecordReplayWindow.TextCfg(WELCOME_TEXT_DE, RECORD_START_INSTRUCTION_DE, IDLE_STATUS_DE))
            return
        
        elif self.state == RECORDING:
            self.setText(RecordReplayWindow.TextCfg(
                RECORDING_STARTED_DE, RECORD_STOP_INSTRUCTION_DE, RECORDING_STATUS_TEXT_BEFORE_S_DE + str(self.remaining_msg) + SECONDS + RECORDING_STATUS_TEXT_AFTER_S_DE
                ))
            return
        
        elif self.state == RESETTING:
            self.setText(RecordReplayWindow.TextCfg(
                NEXT_STEP_RESETTING_DE, RESETTING_STOP_INSTRUCTION_DE, RESETTING_STATUS_TEXT_DE + str(self.remaining_msg) + SECONDS
            ))
            return
        
        elif self.state == REPLAYING:
            self.setText(RecordReplayWindow.TextCfg(
                REPLAYING_STARTED_DE, REPLAY_STOP_INSTRUCTION_DE, REPLAYING_STATUS_TEXT_DE + str(self.remaining_msg) + SECONDS
            ))
            return
        
        elif self.state == FINISHED:
            self.setText(RecordReplayWindow.TextCfg(
                FINISHED_DE, RECORD_START_AGAIN_INSTRUCTION_DE, FINISHED_DE
            ))
            return
        
        # otherwise automatically in READY state
        self.setText(RecordReplayWindow.TextCfg(RECORDING_STOPPED_DE, RECORD_START_INSTRUCTION_DE, READY_STATUS_DE))
        return


    
    def read_output(self):

        try:
            while self.process.canReadLine():
                line = bytes(self.process.readLine()).decode().strip()
                self.handle_message(line)

        except:
            pass



    def handle_message(self, line):

        print("line = ", line)
        try:
            msg = json.loads(line)

        except json.JSONDecodeError:
            raise Exception("json.JSONDecodeError")

        event = msg["event"]

        if event == "recording":

            self.state = RECORDING
            self.remaining_msg = msg["remaining"]
            self.status

            if self.language == EN:
                self.setText(RecordReplayWindow.TextCfg(
                    RECORDING_STARTED_EN, RECORD_STOP_INSTRUCTION_EN, RECORDING_STATUS_TEXT_EN  + str(self.remaining_msg) + SECONDS
                ))

            else:
                self.setText(RecordReplayWindow.TextCfg(
                    RECORDING_STARTED_DE, RECORD_STOP_INSTRUCTION_DE, RECORDING_STATUS_TEXT_BEFORE_S_DE  + str(self.remaining_msg) + SECONDS + RECORDING_STATUS_TEXT_AFTER_S_DE
                ))
            
            publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "RECORDING"}, start_time=self.start_time)

        elif event == "resetting":

            self.state = RESETTING
            self.remaining_msg = msg["remaining"]

            if self.language == EN:
                self.setText(RecordReplayWindow.TextCfg(
                    NEXT_STEP_RESETTING_EN, RESETTING_STOP_INSTRUCTION_EN, RESETTING_STATUS_TEXT_EN + str(self.remaining_msg) + SECONDS
                ))

            else:
                self.setText(RecordReplayWindow.TextCfg(
                    NEXT_STEP_RESETTING_DE , RESETTING_STOP_INSTRUCTION_DE, RESETTING_STATUS_TEXT_DE + str(self.remaining_msg) + SECONDS
                ))

            publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "RESETTING"}, start_time=self.start_time)

        elif event == "replaying":

            self.state = REPLAYING
            self.remaining_msg = msg["remaining"]

            if self.language == EN:
                self.setText(RecordReplayWindow.TextCfg(
                    REPLAYING_STARTED_EN, REPLAY_STOP_INSTRUCTION_EN, REPLAYING_STATUS_TEXT_EN + str(self.remaining_msg) + SECONDS
                ))

            else:
                self.setText(RecordReplayWindow.TextCfg(
                    REPLAYING_STARTED_DE, REPLAY_STOP_INSTRUCTION_DE, REPLAYING_STATUS_TEXT_DE + str(self.remaining_msg) + SECONDS
                ))

            publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "REPLAYING"}, start_time=self.start_time)

        elif event == "finished":

            self.state = FINISHED
            self.stop_button.hide()
            self.start_button.show()
            self.remaining_msg = None

            if self.language == EN:
                self.setText(RecordReplayWindow.TextCfg(
                    FINISHED_EN, RECORD_START_AGAIN_INSTRUCTION_EN, READY_STATUS_EN
                ))
            else:
                self.setText(RecordReplayWindow.TextCfg(
                    FINISHED_DE, RECORD_START_AGAIN_INSTRUCTION_DE, READY_STATUS_DE
                ))

            publish(client=self.system_state_publisher, topic=system_state_topic, data={"state": "READY"}, start_time=self.start_time)

    def setText(self, textCfg: "RecordReplayWindow.TextCfg"):
        self.last_action.setText(textCfg.last_action)
        self.instruction.setText(textCfg.instruction)
        self.status.setText(textCfg.status)



    @dataclass
    class TextCfg:
        last_action: str
        instruction: str
        status: str

from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QTextCursor

from publisher import USBPublisher, ServoPublisher

from lerobot.constants import REST_POSE
from lerobot.motor_read_write import check_connection, read_test_leader, read_test_follower, set_rest_pose, TeleoperateConfig

from lerobot.common.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.common.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig

from constants import (
    EN, DE,

    SETUP_TITLE_EN, SETUP_TITLE_DE,

    COLOR_SUCCESS,
    COLOR_ADVICE,
    COLOR_ERROR,
    COLOR_STANDARD,

    CONNECTED_EN, CONNECTED_DE,
    NOT_CONNECTED_EN, NOT_CONNECTED_DE,

    STM_POWER_EN, STM_POWER_DE,

    CHECK_USB_EN, CHECK_USB_DE,
    USB_STATE_EN, USB_STATE_DE,
    LEADER_USB_OK_EN, LEADER_USB_OK_DE,
    LEADER_USB_FAIL_EN, LEADER_USB_FAIL_DE,
    FOLLOWER_USB_OK_EN, FOLLOWER_USB_OK_DE,
    FOLLOWER_USB_FAIL_EN, FOLLOWER_USB_FAIL_DE,
    LEADER_AND_FOLLOWER_USB_FAIL_EN, LEADER_AND_FOLLOWER_USB_FAIL_DE,
    USB_OK_EN, USB_OK_DE,

    READING_SERVO_POSITIONS_EN, READING_SERVO_POSITIONS_DE,


    SERVO_CHECK_EN, SERVO_CHECK_DE,
    SERVO_STATE_EN, SERVO_STATE_DE,
    SERVO_CONNECTED_EN, SERVO_CONNECTED_DE,
    LEADER_SERVO_OK_EN, LEADER_SERVO_OK_DE,
    LEADER_SERVO_FAIL_EN, LEADER_SERVO_FAIL_DE,
    FOLLOWER_SERVO_OK_EN, FOLLOWER_SERVO_OK_DE,
    FOLLOWER_SERVO_FAIL_EN, FOLLOWER_SERVO_FAIL_DE,
    LEADER_AND_FOLLOWER_SERVO_FAIL_EN, LEADER_AND_FOLLOWER_SERVO_FAIL_DE,
    READING_SERVO_POSITIONS_EN, READING_SERVO_POSITIONS_DE,
    READING_LEADER_OK_EN, READING_LEADER_OK_DE,
    READING_FOLLOWER_OK_EN, READING_FOLLOWER_OK_DE,
    MOVE_TO_REST_POSE_EN, MOVE_TO_REST_POSE_DE,
    REACHED_REST_POSE_EN, REACHED_REST_POSE_DE,
    REST_POSE,
    SERVO_FAIL_EN, SERVO_FAIL_DE,
    SERVO_OK_EN, SERVO_OK_DE,

    SETUP_DONE_EN, SETUP_DONE_DE
)





class SetupWindow(QWidget):

    def __init__(self, language):
        super().__init__()

        # general settings
        self.language = language
        self.process = None
        self.run_id = 0

        # set task state
        self.task1_ok = False
        self.task2_ok = False
        self.task3_ok = False

        # set USB states
        self.usb_check_started = False
        self.last_usb_state = (None, None)

        # USB thread
        self.usb = None

        # set servo states
        self.servo_check_started = False
        self.last_servo_state = (None, None)

        # servo config
        self.servo_cfg = TeleoperateConfig(
            robot=SO101FollowerConfig(
                port="/dev/so-follower",
                id="my_follower",
            ),
            teleop=SO101LeaderConfig(
                port="/dev/so-leader",
                id="my_leader",
            ),
            display_data=False,
        )

        # servo thread
        self.servo = None

        # initialize empty page layout - not self.layout because it would overwrite layout from MainWindow!
        layout = QVBoxLayout()

        # title
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # log window
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
            QTextEdit {
                background-color: #111;
                color: #ddd;
                font-family: monospace;
                font-size: 11px;
                border: none;
            }
        """)
        self.log.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(self.log)

        self.setLayout(layout)

        # init texts + start
        self.update_texts()
        self.start()



    def start(self):

        self.stop()

        self.run_id += 1
        current_run = self.run_id

        self.task1_ok = True
        self.task2_ok = False
        self.task3_ok = False

        self.usb_check_started = False
        self.servo_check_started = False

        self.last_usb_state = (None, None)
        self.last_servo_state = (None, None)

        self.usb = USBPublisher()
        self.usb.usb_changed.connect(self.usb_changed)

        self.servo = ServoPublisher(self.servo_cfg)
        self.servo.servo_changed.connect(self.servo_changed)

        self.log.clear()

        self.append_log(self.set_text(STM_POWER_EN, STM_POWER_DE), COLOR_SUCCESS, bold=True)
        self.append_log("")

        QTimer.singleShot(500, lambda: self.start_usb(current_run))


    def stop(self):

        if self.process is not None:
            if self.process.state() != QProcess.NotRunning:
                self.process.kill()
            self.process = None

        if self.usb is not None:

            if self.usb.isRunning():
                self.usb.stop()
                self.usb.wait()

            self.usb = None

        if self.servo is not None:

            if self.servo.isRunning():
                self.servo.stop()
                self.servo.wait()

            self.servo = None



    def start_usb(self, run_id):

        if run_id != self.run_id:
            return

        self.usb_check_started = True

        if not self.usb.isRunning():
            self.usb.start()

        self.append_log(self.set_text(CHECK_USB_EN, CHECK_USB_DE))


    def usb_changed(self, leader, follower, run_id=None):

        if run_id is None:
            run_id = self.run_id

        if run_id != self.run_id:
            return

        if self.task2_ok:
            return

        if not self.usb_check_started:
            return

        state_changed = (leader, follower) != self.last_usb_state

        self.last_usb_state = (leader, follower)

        if not state_changed:
            return

        leader_text = self.set_text(
            CONNECTED_EN if leader else NOT_CONNECTED_EN,
            CONNECTED_DE if leader else NOT_CONNECTED_DE
        )

        follower_text = self.set_text(
            CONNECTED_EN if follower else NOT_CONNECTED_EN,
            CONNECTED_DE if follower else NOT_CONNECTED_DE
        )

        self.append_log(self.set_text(USB_STATE_EN, USB_STATE_DE).format(leader=leader_text, follower=follower_text))


        if leader and follower:

            self.append_log("")
            self.append_log(self.set_text(USB_OK_EN, USB_OK_DE), COLOR_SUCCESS, bold=True)

            self.task2_ok = True

            QTimer.singleShot(500, lambda: self.start_servo(run_id))

            return


        if leader and not follower:

            self.append_log("")
            self.append_log(self.set_text(LEADER_USB_OK_EN, LEADER_USB_OK_DE), COLOR_SUCCESS)
            self.append_log(self.set_text(FOLLOWER_USB_FAIL_EN, FOLLOWER_USB_FAIL_DE), COLOR_ADVICE, italic=True)
            self.append_log("")
            self.append_log(self.set_text(CHECK_USB_EN, CHECK_USB_DE))

            return


        if follower and not leader:

            self.append_log("")
            self.append_log(self.set_text(FOLLOWER_USB_OK_EN, FOLLOWER_USB_OK_DE), COLOR_SUCCESS)
            self.append_log(self.set_text(LEADER_USB_FAIL_EN, LEADER_USB_FAIL_DE), COLOR_ADVICE, italic=True)
            self.append_log("")
            self.append_log(self.set_text(CHECK_USB_EN, CHECK_USB_DE))

            return


        if not leader and not follower:

            self.append_log("")
            self.append_log(self.set_text(LEADER_AND_FOLLOWER_USB_FAIL_EN, LEADER_AND_FOLLOWER_USB_FAIL_DE), COLOR_ADVICE, italic=True)
            self.append_log("")
            self.append_log(self.set_text(CHECK_USB_EN, CHECK_USB_DE))

            return


    def start_servo(self, run_id):

        if run_id != self.run_id:
            return

        self.servo_check_started = True

        self.append_log("")
        self.append_log(self.set_text(SERVO_CHECK_EN, SERVO_CHECK_DE))

        if not self.servo.isRunning():
            self.servo.start()


    def servo_changed(self, leader, follower, run_id=None):

        if run_id is None:
            run_id = self.run_id

        if run_id != self.run_id:
            return

        if self.task3_ok:
            return

        state_changed = (leader, follower) != self.last_servo_state

        self.last_servo_state = (leader, follower)

        if not state_changed:
            return

        if not self.servo_check_started:
            return

        leader_text = self.set_text(
            CONNECTED_EN if leader else NOT_CONNECTED_EN,
            CONNECTED_DE if leader else NOT_CONNECTED_DE
        )

        follower_text = self.set_text(
            CONNECTED_EN if follower else NOT_CONNECTED_EN,
            CONNECTED_DE if follower else NOT_CONNECTED_DE
        )

        self.append_log(self.set_text(SERVO_STATE_EN, SERVO_STATE_DE).format(leader=leader_text, follower=follower_text))


        if leader and follower:

            self.append_log("")
            self.append_log(self.set_text(SERVO_CONNECTED_EN, SERVO_CONNECTED_DE), COLOR_SUCCESS)

            QTimer.singleShot(500, lambda: self.run_servo_tests())
            return


        if leader and not follower:

            self.append_log("")
            self.append_log(self.set_text(LEADER_SERVO_OK_EN, LEADER_SERVO_OK_DE), COLOR_SUCCESS)
            self.append_log(self.set_text(FOLLOWER_SERVO_FAIL_EN, FOLLOWER_SERVO_FAIL_DE), COLOR_ADVICE, italic=True)
            self.append_log("")
            self.append_log(self.set_text(SERVO_CHECK_EN, SERVO_CHECK_DE))

            return


        if follower and not leader:

            self.append_log("")
            self.append_log(self.set_text(FOLLOWER_SERVO_OK_EN, FOLLOWER_SERVO_OK_DE), COLOR_SUCCESS)
            self.append_log(self.set_text(LEADER_SERVO_FAIL_EN, LEADER_SERVO_FAIL_DE), COLOR_ADVICE, italic=True)
            self.append_log("")
            self.append_log(self.set_text(SERVO_CHECK_EN, SERVO_CHECK_DE))

            return


        if not leader and not follower:

            self.append_log("")
            self.append_log(self.set_text(LEADER_AND_FOLLOWER_SERVO_FAIL_EN, LEADER_AND_FOLLOWER_SERVO_FAIL_DE), COLOR_ADVICE, italic=True)
            self.append_log("")
            self.append_log(self.set_text(SERVO_CHECK_EN, SERVO_CHECK_DE))


    def run_servo_tests(self):

        teleop = None
        robot = None

        try:
            success, teleop, robot = check_connection(self.servo_cfg)

            if not success:
                raise Exception("Connection failed")

            self.append_log("")
            self.append_log(self.set_text(READING_SERVO_POSITIONS_EN, READING_SERVO_POSITIONS_DE))

            try:
                read_test_leader(teleop)
                self.append_log(self.set_text(READING_LEADER_OK_EN, READING_LEADER_OK_DE), COLOR_SUCCESS)
            except Exception as e:
                raise Exception(f"Leader read failed: {e}")

            try:
                read_test_follower(robot)
                self.append_log(self.set_text(READING_FOLLOWER_OK_EN, READING_FOLLOWER_OK_DE), COLOR_SUCCESS)
            except Exception as e:
                raise Exception(f"Follower read failed: {e}")

            self.append_log("")
            self.append_log(self.set_text(MOVE_TO_REST_POSE_EN, MOVE_TO_REST_POSE_DE))

            set_rest_pose(
                teleop,
                robot,
                REST_POSE,
                self.servo_cfg.fps,
                duration=3,
            )

            self.append_log(self.set_text(REACHED_REST_POSE_EN, REACHED_REST_POSE_DE), COLOR_SUCCESS)

            self.task3_ok = True

            self.append_log("")
            self.append_log(self.set_text(SERVO_OK_EN, SERVO_OK_DE), COLOR_SUCCESS, bold=True)

            self.check_done()

        except Exception as e:
            self.append_log("")
            self.append_log(f"{self.set_text(SERVO_FAIL_EN, SERVO_FAIL_DE)}: {e}", COLOR_ERROR, bold=True)

        finally:
            try:
                teleop.disconnect()
            except:
                pass

            try:
                robot.disconnect()
            except:
                pass



    def check_done(self):

        if self.task1_ok and self.task2_ok and self.task3_ok:
            self.append_log("")
            self.append_log(self.set_text(SETUP_DONE_EN, SETUP_DONE_DE), COLOR_SUCCESS, bold=True)



    def update_texts(self):
        self.title.setText(self.set_text(SETUP_TITLE_EN, SETUP_TITLE_DE))



    def update_language(self, language):

        if self.language == language:
            return

        self.language = language
        self.update_texts()



    def set_english(self):

        if self.language == EN:
            return

        self.language = EN
        self.update_texts()
        self.start()


    def set_german(self):

        if self.language == DE:
            return

        self.language = DE
        self.update_texts()
        self.start()



    def set_text(self, en, de):
        return en if self.language == EN else de



    def append_log(self, text, color=COLOR_STANDARD, bold=False, italic=False):

        style = f"color:{color};"

        if bold:
            style += "font-weight:bold;"
        if italic:
            style += "font-style:italic;"

        html = f'<span style="{style}">{text}</span><br>'

        self.log.moveCursor(QTextCursor.End)
        self.log.insertHtml(html)
        self.log.moveCursor(QTextCursor.End)

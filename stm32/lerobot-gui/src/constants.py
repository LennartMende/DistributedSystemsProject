# window IDs
SETUP_WINDOW = 0
TELEOP_WINDOW = 1
RECORD_REPLAY_WINDOW = 2

# status ids
IDLE = 0
TELEOPERATING = 1
READY = 2 
RECORDING = 3
REPLAYING = 4
FINISHED = 5
RESETTING = 6
CONNECTING = 7

# window size
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 272

# language buttons
EN = "EN"
DE = "DE"

# mode tabs
TELEOP = "TELEOP"
RECORD_REPLAY = "RECORD && REPLAY"


# colors
COLOR_STANDARD = "#ffffff"
COLOR_SUCCESS = "#00ff88"
COLOR_ADVICE = "#ff8c00"
COLOR_ERROR = "#ff4444"


# text for system setup
SETUP_TITLE_EN = "System setup instructions"
SETUP_TITLE_DE = "Hinweise zur Systemeinrichtung"

STM_POWER_EN = "STM is powered (1|3)"
STM_POWER_DE = "STM wird mit Strom versorgt (1|3)"

CHECK_USB_EN = "Checking USB connections ..."
CHECK_USB_DE = "Überprüfe USB-Verbindungen ..."

USB_STATE_EN = "USB states - Leader: {leader}, Follower: {follower}"
USB_STATE_DE = "USB Status - Leader: {leader}, Follower: {follower}"

CONNECTED_EN = "connected"
CONNECTED_DE = "verbunden"

NOT_CONNECTED_EN = "not connected"
NOT_CONNECTED_DE = "nicht verbunden"

LEADER_USB_OK_EN = "Leader connected successfully via USB"
LEADER_USB_OK_DE = "Leader erfolgreich über USB verbunden"

LEADER_USB_FAIL_EN = "Leader is not connected, please connect it via USB"
LEADER_USB_FAIL_DE = "Leader ist nicht verbunden, bitte über USB verbinden"

FOLLOWER_USB_OK_EN = "Follower connected successfully via USB"
FOLLOWER_USB_OK_DE = "Follower erfolgreich über USB verbunden"

FOLLOWER_USB_FAIL_EN = "Follower is not connected, please connect it via USB"
FOLLOWER_USB_FAIL_DE = "Follower ist nicht verbunden, bitte über USB verbinden"

LEADER_AND_FOLLOWER_USB_FAIL_EN = "Leader and Follower are not connected, please connect both via USB"
LEADER_AND_FOLLOWER_USB_FAIL_DE = "Leader und Follower sind nicht verbunden, bitte beide über USB verbinden"

USB_OK_EN = "Leader and Follower detected succesfully as USB devices (2|3)"
USB_OK_DE = "Leader und Follower erfolgreich als USB-Geräte erkannt (2|3)"

SERVO_CHECK_EN = "Checking servos ..."
SERVO_CHECK_DE = "Überprüfe Servomotoren ..."

SERVO_STATE_EN = "Servo states - Leader: {leader}, Follower: {follower}"
SERVO_STATE_DE = "Servo Status - Leader: {leader}, Follower: {follower}"

LEADER_SERVO_OK_EN = "Leader servo motors connected successfully"
LEADER_SERVO_OK_DE = "Leader Servomotoren erfolgreich verbunden"

LEADER_SERVO_FAIL_EN = "Leader servo motors are not connected, please connect Leader to power"
LEADER_SERVO_FAIL_DE = "Leader Servomotoren sind nicht verbunden, bitte Leader an die Stromversorgung anschließen"

FOLLOWER_SERVO_OK_EN = "Follower servo motors connected successfully"
FOLLOWER_SERVO_OK_DE = "Follower Servomotoren erfolgreich verbunden"

FOLLOWER_SERVO_FAIL_EN = "Follower servo motors are not connected, please connect Follower to power"
FOLLOWER_SERVO_FAIL_DE = "Follower Servomotoren sind nicht verbunden, bitte Follower an die Stromversorgung anschließen"

LEADER_AND_FOLLOWER_SERVO_FAIL_EN = "Leader and Follower servo motors are not connected, please connect Leader and Follower to power"
LEADER_AND_FOLLOWER_SERVO_FAIL_DE = "Leader und Follower Servomotoren sind nicht verbunden, bitte Leader and Follower an die Stromversorgung anschließen"

SERVO_CONNECTED_EN = "Leader and Follower servo motors connected successfully"
SERVO_CONNECTED_DE = "Leader and Follower Servomotoren erfolgreich verbunden"

SERVO_FAIL_EN = "Connection to servo motors failed"
SERVO_FAIL_DE = "Verbindung zu den Servomotoren fehlgeschlagen"

READING_SERVO_POSITIONS_EN = "Reading position of all servo motors ..."
READING_SERVO_POSITIONS_DE = "Positionen aller Servomotoren werden gelesen ..."

READING_LEADER_OK_EN = "Reading position of Leader servo motors successful"
READING_LEADER_OK_DE = "Position der Leader Servomotoren erfolgreich gelesen"

READING_FOLLOWER_OK_EN = "Reading position of Follower servo motors successful"
READING_FOLLOWER_OK_DE = "Positionen der Follower Servomotoren erfolgreich gelesen"

MOVE_TO_REST_POSE_EN = "Moving Follower to rest pose ..."
MOVE_TO_REST_POSE_DE = "Follower wird in die Ruhepose bewegt ..."

REACHED_REST_POSE_EN = "Follower reached rest pose"
REACHED_REST_POSE_DE = "Follower hat Ruhepose erreicht"

SERVO_OK_EN = "Servo motors responding, Follower in rest pose (3|3)"
SERVO_OK_DE = "Servomotoren antworten, Follower in Ruhepose (3|3)"

SETUP_DONE_EN = "System setup completed successfully"
SETUP_DONE_DE = "System-Setup erfolgreich abgeschlossen"


# rest pose follower
REST_POSE = {
    'shoulder_pan.pos': 4.076386338597132,
    'shoulder_lift.pos': -97.59933774834437,
    'elbow_flex.pos': 98.49889624724062,
    'wrist_flex.pos': 54.75074563272261,
    'wrist_roll.pos': 0.884495317377727,
    'gripper.pos': 2.976190476190476
}


# welcome text
WELCOME_TEXT_EN = "Welcome to SO-ARM 101"
WELCOME_TEXT_DE = "Willkommen bei SO-ARM 101"

# last teleoperation action
TELEOPERATION_STARTED_EN = "Teleoperation started"
TELEOPERATION_STARTED_DE = "Teleoperation gestartet"

TELEOPERATION_STOPPED_EN = "Teleoperation stopped"
TELEOPERATION_STOPPED_DE = "Teleoperation gestoppt"

# last record and replay action
RECORDING_STARTED_EN = "Recording started"
RECORDING_STARTED_DE = "Aufnahme gestartet"

RECORDING_STOPPED_EN = "Recording aborted"
RECORDING_STOPPED_DE = "Aufnehmen abgebrochen"


# last actions
RECORDING_FINISHED_EN = "Recording finished"
RECORDING_FINISHED_DE = "Aufnahme abgeschlossen"

NEXT_STEP_RESETTING_EN = "Next step requires resetting"
NEXT_STEP_RESETTING_DE = "Nächster Schritt setzt Reset voraus"

REPLAYING_STARTED_EN = "Replaying started"
REPLAYING_STARTED_DE = "Wiederholung gestartet"

FINISHED_EN = "Finished recording and replaying"
FINISHED_DE = "Aufnahme und Wiederholung abgeschlossen"


# teleoperation instructions
TELEOPERATION_START_INSTRUCTION_EN = "Press the button to start teleoperation"
TELEOPERATION_START_INSTRUCTION_DE = "Drücken Sie den Knopf, um die Teleoperation zu starten"

TELEOPERATION_STOP_INSTRUCTION_EN = "Press the button to abort teleoperation"
TELEOPERATION_STOP_INSTRUCTION_DE = "Drücken Sie den Knopf, um die Teleoperation abzubrechen"


# record start instructions
RECORD_START_INSTRUCTION_EN = "Press the button to start recording"
RECORD_START_INSTRUCTION_DE = "Drücken Sie den Knopf, um die Aufnahme zu starten"

# record again instructions
RECORD_START_AGAIN_INSTRUCTION_EN = "Press the button to start recording again"
RECORD_START_AGAIN_INSTRUCTION_DE = "Drücken Sie den Knopf, um die Aufnahme erneut zu starten"

# record abort instructions
RECORD_STOP_INSTRUCTION_EN = "Press the button to abort recording"
RECORD_STOP_INSTRUCTION_DE = "Drücken Sie den Knopf, um die Aufnahme abzubrechen"

# reset abort instruction
RESETTING_STOP_INSTRUCTION_EN = "Press the button to abort resetting"
RESETTING_STOP_INSTRUCTION_DE = "Drücken Sie den Knopf, um den Reset abzubrechen"


# replay abort instructions
REPLAY_STOP_INSTRUCTION_EN = "Press the button to abort replaying"
REPLAY_STOP_INSTRUCTION_DE = "Drücken Sie den Knopf, um das Wiederholen abzubrechen"


# status texts
IDLE_STATUS_EN = "Idle mode"
IDLE_STATUS_DE = "Ruhezustand"

TELEOPERATING_STATUS_EN = "Teleoperating"
TELEOPERATING_STATUS_DE = "Teleoperation aktiv"

SECONDS = " s"

RECORDING_STATUS_TEXT_EN = "Recording continues for "
RECORDING_STATUS_START_EN = "Connecting to servo motors"
RECORDING_STATUS_TEXT_BEFORE_S_DE = "Nimmt "
RECORDING_STATUS_TEXT_AFTER_S_DE = " auf"
RECORDING_STATUS_START_DE = "Verbindung zu Servomotoren wird aufgebaut"

RESETTING_STATUS_TEXT_EN = "Resetting "
RESETTING_STATUS_TEXT_DE = "Resettet "

RESETTING_STATUS_TELEOP_EN = "Resetting "
RESETTING_STATUS_TELEOP_DE = "Resettet "

RESETTING_STOP_INSTRUCTION_EN = "Press the button to abort resetting"
RESETTING_STOP_INSTRUCTION_DE = "Drücken Sie den Knopf, um den Reset abzubrechen"

REPLAYING_STATUS_TEXT_EN = "Replaying for "
REPLAYING_STATUS_TEXT_DE = "Wiederholt "

READY_STATUS_EN = "Ready"
READY_STATUS_DE = "Bereit"

# Connection labels
CONNECTION_STATUS_EN = "Connecting to servo motors"
CONNECTION_STATUS_DE = "Verbindungsaufbau zu Servomotoren"

CONNECTION_STOP_INSTRUCTION_EN = "Press the button to abort connection"
CONNECTION_STOP_INSTRUCTION_DE = "Drücken Sie den Knopf, um den Verbindungaufbau abzubrechen"

CONNECTION_FINISHED_TEXT_EN = "Connecting to servo motors finished"
CONNECTION_FINISHED_TEXT_DE = "Verbindungsaufbau beendet"

# directories
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "images")


# images
LOGO_HTWK_FILE = os.path.join(IMG_DIR, "logo_HTWK.png")
SETUP_BUTTON_BLACK_FILE = os.path.join(IMG_DIR, "setup_button_black.png")
SETUP_BUTTON_ORANGE_FILE = os.path.join(IMG_DIR, "setup_button_orange.png")
START_BUTTON_ICON_FILE = os.path.join(IMG_DIR, "start_button.png")
STOP_BUTTON_ICON_FILE = os.path.join(IMG_DIR, "stop_button.png")



# commands
TELEOP_COMMAND = [
    "python3",
    "-m",
    "lerobot.teleoperate",
    "--robot.type=so101_follower",
    "--robot.port=/dev/so-follower",
    "--robot.id=my_follower",
    "--teleop.type=so101_leader",
    "--teleop.port=/dev/so-leader",
    "--teleop.id=my_leader",
    "--display_data=false",
]

RECORD_REPLAY_COMMAND = [
    "python3",
    "-u",
    "-m",
    "lerobot.record_and_replay",
    "--robot.type=so101_follower",
    "--robot.port=/dev/so-follower",
    "--robot.id=my_follower",
    "--teleop.type=so101_leader",
    "--teleop.port=/dev/so-leader",
    "--teleop.id=my_leader",
    "--display_data=false",
]

MOTOR_READ_WRITE_COMMAND = [
    "-m",
    "lerobot.motor_read_write",
    "--robot.type=so101_follower",
    "--robot.port=/dev/so-follower",
    "--robot.id=my_follower",
    "--teleop.type=so101_leader",
    "--teleop.port=/dev/so-leader",
    "--teleop.id=my_leader",
    "--display_data=false",
]

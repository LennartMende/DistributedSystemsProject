# settings for record and replay
SLEEP_DURATION = 5
RECORD_DURATION = 20
FPS = 60


# rest pose follower
REST_POSE = {
    'shoulder_pan.pos': 4.076386338597132,
    'shoulder_lift.pos': -97.59933774834437,
    'elbow_flex.pos': 98.49889624724062,
    'wrist_flex.pos': 54.75074563272261,
    'wrist_roll.pos': 0.884495317377727,
    'gripper.pos': 2.976190476190476
}



# networking.py
#BROKER = "192.168.7.27"
BROKER = "localhost"
PORT = 1883 # 8883 for secure MQTT
USERNAME = "username"
PASSWORD = "password"

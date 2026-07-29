import os
import subprocess
import time

from lerobot.utils import ClientCfg, State, subscribe_in_thread
from lerobot.utils import connect as connect_client

# create a subscriber for slider control
dashboard_mode_topic = "dashboard_mode"
client_id = 'dashboard_mode_subscriber'
clientCfg = ClientCfg(client_id=client_id)
dashboard_mode_subscriber = connect_client(clientCfg=clientCfg)

# create a state variable for pointer like manipulation
dashboard_mode: State = State(data_str="mode")

# set subscription to run concurrently
subscribe_in_thread(dashboard_mode_subscriber, dashboard_mode_topic, dashboard_mode)

last_dashboard_mode: None | str = None

process = None
process_type: str = "None"

#####
# TERMINATE, KILL OR SYSTEMCL STOP THE PROCESSES? MAKE THIS TO LEROBOT-GUI SERVICE???
#####

while True:
    while dashboard_mode.data is None:
        time.sleep(0.01)

    if dashboard_mode.data == "observe" and last_dashboard_mode != "observe":
        if process is not None:
            process.terminate()
        process = subprocess.Popen("python3", "-u", "/opt/lerobot-gui/src/app.py")
        last_dashboard_mode = "observe"
        #process_type = "OBSERVE"

    elif dashboard_mode.data == "control" and last_dashboard_mode != "control":
        if process is not None:
            process.terminate()
        process = subprocess.Popen("python3", "-u", "control_conflict_window.py", "control") # WICHTIG: sys.argv[1] == "control" PROBABLY NOT THE CASE WHEN RUNNING WITH -u
        last_dashboard_mode = "control"

    elif dashboard_mode.data == "conflict" and last_dashboard_mode != "conflict":
        if process is not None:
            process.terminate()
        process = subprocess.Popen("python3", "-u", "control_conflict_window.py", "conflict") # WICHTIG: sys.argv[1] == "conflict" PROBABLY NOT THE CASE WHEN RUNNING WITH -u
        last_dashboard_mode = "conflict"

    else:
        raise ValueError

    time.sleep(0.01)
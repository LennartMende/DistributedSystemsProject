import os
import subprocess
import time

from lerobot.utils import ClientCfg, State, subscribe_in_thread
from lerobot.utils import connect as connect_client

dashboard_active = False

try:
    # create a subscriber for slider control
    dashboard_mode_topic = "dashboard_mode"
    client_id = 'dashboard_mode_subscriber'
    clientCfg = ClientCfg(client_id=client_id)
    dashboard_mode_subscriber = connect_client(clientCfg=clientCfg)
    dashboard_active = True
except:
    dashboard_active = False

if dashboard_active:
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

        if dashboard_mode.data == last_dashboard_mode:
            time.sleep(0.01)
            continue

        elif dashboard_mode.data == "observe":
            if process is not None:
                process.terminate()

            process = subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/app.py"])
            last_dashboard_mode = "observe"

        elif dashboard_mode.data == "control":
            if process is not None:
                process.terminate()

            process = subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/control_conflict_window.py", "control"])
            last_dashboard_mode = "control"

        elif dashboard_mode.data == "conflict":
            if process is not None:
                process.terminate()

            process = subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/control_conflict_window.py", "conflict"])
            last_dashboard_mode = "conflict"

        else:
            if process is not None:
                process.terminate()

            process = subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/app.py"])
            last_dashboard_mode = dashboard_mode.data

        time.sleep(0.01)

else:
    subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/app.py"])
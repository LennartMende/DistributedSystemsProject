import signal
import sys
import os
import subprocess
import time

from lerobot.utils import ClientCfg, State, subscribe_in_thread
from lerobot.utils import connect as connect_client

def cleanup(sig, frame):
    global process

    print("Stopping...")

    if process is not None:
        process.terminate()

        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

dashboard_active = False

print("Begin of dashboard_mode_control.py")

try:
    # create a subscriber for slider control
    dashboard_mode_topic = "dashboard/mode"
    client_id = 'dashboard_mode_subscriber'
    clientCfg = ClientCfg(client_id=client_id)
    dashboard_mode_subscriber = connect_client(clientCfg=clientCfg)
    dashboard_active = True
    print("GUI uses dashboard subscriber")
except:
    dashboard_active = False
    print("GUI doesn't use dashboard subscriber")

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
        if dashboard_mode.data == last_dashboard_mode:
            time.sleep(0.01)
            continue

        elif (dashboard_mode.data == "observe" or dashboard_mode.data is None):
            print("[DASHBOARD MODE] observe")
            if process is not None:
                process.terminate()

                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

            #process = subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/app.py"])
            process = subprocess.Popen([
                "/usr/bin/python3",
                "-u",
                "/opt/lerobot-gui/src/app.py"
            ])
            last_dashboard_mode = "observe"

        elif dashboard_mode.data == "control":
            print("[DASHBOARD MODE] control")
            if process is not None:
                process.terminate()

                try:                                                                       
                    process.wait(timeout=1)                                                
                except subprocess.TimeoutExpired:                                          
                    process.kill()                                                         
                    process.wait()

            process = subprocess.Popen([
                "/usr/bin/python3",
                "-u",
                "/opt/lerobot-gui/src/control_conflict_window.py",
                "control"
            ]) 
            last_dashboard_mode = "control"

        elif dashboard_mode.data == "conflict":
            print("[DASHBOARD MODE] conflict")
            if process is not None:
                process.terminate()

                try:                                                                       
                    process.wait(timeout=1)                                                
                except subprocess.TimeoutExpired:                                          
                    process.kill()                                                         
                    process.wait()

            process = subprocess.Popen([
                "/usr/bin/python3",
                "-u",
                "/opt/lerobot-gui/src/control_conflict_window.py",
                "conflict"
            ])
            last_dashboard_mode = "conflict"

        else:
            if process is not None:
                process.terminate()

            process = subprocess.Popen(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/app.py"])
            last_dashboard_mode = dashboard_mode.data

        time.sleep(0.01)

else:
    subprocess.run(["/usr/bin/python3", "-u", "/opt/lerobot-gui/src/app.py"])


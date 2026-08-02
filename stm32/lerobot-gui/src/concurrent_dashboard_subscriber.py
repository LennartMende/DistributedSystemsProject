import os
import subprocess
import time

from lerobot.utils import ClientCfg, State, subscribe_in_thread
from lerobot.utils import connect as connect_client

dashboard_active = False

try:
    # create a subscriber for slider control
    dashboard_mode_topic = "dashboard/mode"
    client_id = 'dashboard_mode_subscriber'
    clientCfg = ClientCfg(client_id=client_id)
    dashboard_mode_subscriber = connect_client(clientCfg=clientCfg)
    dashboard_active = True
except:
    dashboard_active = False
finally:
    print("dashboard_active = ", dashboard_active)

if dashboard_active:
    print("Dashboard active")
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
            print("[SUBSCRIBER] Dashboard mode changed to observe mode")
            last_dashboard_mode = "observe"

        elif dashboard_mode.data == "control":
            print("[SUBSCRIBER] Dashboard mode changed to control mode")

            last_dashboard_mode = "control"

        elif dashboard_mode.data == "conflict":
            print("[SUBSCRIBER] Dashboard mode changed to confilct")

            last_dashboard_mode = "conflict"

        else:
            print("[SUBSCRIBER] Dashboard in else mode")
            last_dashboard_mode = dashboard_mode.data

        time.sleep(0.01)

else:
    while True:
        print("Rimen is gay")
        time.sleep(1)

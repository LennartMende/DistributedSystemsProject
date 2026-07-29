"""
```shell
python3 -m lerobot.teleoperate --robot.type=so101_follower --robot.port=/dev/so-follower --robot.id=my_follower --teleop.type=so101_leader --teleop.port=/dev/so-leader --teleop.id=my_leader
```
"""

import time
import draccus

from dataclasses import dataclass

from lerobot.common.robots import Robot, RobotConfig, make_robot_from_config
from lerobot.common.teleoperators import Teleoperator, TeleoperatorConfig,make_teleoperator_from_config
from lerobot.common.utils.robot_utils import busy_wait
from lerobot.common.utils.utils import init_logging

from lerobot.constants import REST_POSE#, BROKER, PORT, USERNAME, PASSWORD
from lerobot.utils import ClientCfg, State, subscribe_in_thread, publish
from lerobot.utils import connect as connect_client
from lerobot.motor_read_write import set_rest_pose

# the following imports are not neccesary for the script itself, but for shell command and argument parsing via draccus
from lerobot.common.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.common.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig





@dataclass
class TeleoperateConfig:
    teleop: TeleoperatorConfig
    robot: RobotConfig
    fps: int = 60
    teleop_time_s: float | None = None
    display_data: bool = False



# create a subscriber for slider control
controller_topic = "control"
client_id = 'control_subscriber'
clientCfg = ClientCfg(client_id=client_id)
control_subscriber = connect_client(clientCfg=clientCfg)

# create a state variable for pointer like manipulation
state: State = State()

# set subscription to run concurrently
subscribe_in_thread(control_subscriber, controller_topic, state)

# state
system_state_topic = "system/state"
client_id = 'leader_state_publisher'
clientCfg = ClientCfg(client_id=client_id)
system_state_publisher = connect_client(clientCfg=clientCfg)
publish(client=system_state_publisher, topic=system_state_topic, data={"state" : "RUNNING"}, start_time=time.perf_counter())

def teleop_loop(
    teleop: Teleoperator, robot: Robot, fps: int, display_data: bool = False, duration: float | None = None
):
    
    start_time = time.perf_counter()

    while True:
        loop_start = time.perf_counter()

        while state.data is None:
            time.sleep(0.01)
        robot.send_action(state.data)
        dt_s = time.perf_counter() - loop_start


        busy_wait(1 / fps - dt_s)

        loop_s = time.perf_counter() - loop_start
        
        print(f"\ntime: {loop_s * 1e3:.2f}ms ({1 / loop_s:.0f} Hz)")

        if duration is not None and time.perf_counter() - start_time >= duration:
            return



@draccus.wrap()
def teleoperate(cfg: TeleoperateConfig):

    init_logging()

    teleop = make_teleoperator_from_config(cfg.teleop)
    robot = make_robot_from_config(cfg.robot)

    teleop.connect()
    robot.connect()

    print("CONNECTED", flush=True)
    publish(client=system_state_publisher, topic=system_state_topic, data={"state" : "RESETTING"}, start_time=time.perf_counter())
 
    set_rest_pose(teleop=teleop, robot=robot, rest_pose=REST_POSE, fps=cfg.fps)

    print("READY", flush=True)
    publish(client=system_state_publisher, topic=system_state_topic, data={"state" : "RUNNING"}, start_time=time.perf_counter())
    try:
        teleop_loop(teleop, robot, cfg.fps, display_data=cfg.display_data, duration=cfg.teleop_time_s)
    except KeyboardInterrupt:
        pass





if __name__ == "__main__":
    teleoperate()

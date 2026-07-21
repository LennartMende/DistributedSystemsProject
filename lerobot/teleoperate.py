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

from lerobot.constants import REST_POSE, BROKER, PORT, USERNAME, PASSWORD
from lerobot.utils import ClientCfg, publish
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


# create clients
# positions
follower_pos_topic = "follower/pos"
client_id = 'follower_pos_publisher'
clientCfg = ClientCfg(client_id=client_id, port=PORT, broker=BROKER, username=USERNAME, password=PASSWORD)
follower_pos_publisher = connect_client(clientCfg=clientCfg)

leader_pos_topic = "leader/pos"
client_id = 'leader_pos_publisher'
clientCfg = ClientCfg(client_id=client_id, port=PORT, broker=BROKER, username=USERNAME, password=PASSWORD)
leader_pos_publisher = connect_client(clientCfg=clientCfg)

# temperatures
follower_temp_topic = "follower/temp"
client_id = 'follower_temp_publisher'
clientCfg = ClientCfg(client_id=client_id, port=PORT, broker=BROKER, username=USERNAME, password=PASSWORD)
follower_temp_publisher = connect_client(clientCfg=clientCfg)

leader_temp_topic = "leader/temp"
client_id = 'leader_temp_publisher'
clientCfg = ClientCfg(client_id=client_id, port=PORT, broker=BROKER, username=USERNAME, password=PASSWORD)
leader_temp_publisher = connect_client(clientCfg=clientCfg)

# voltages
follower_volt_topic = "follower/volt"
client_id = 'follower_volt_publisher'
clientCfg = ClientCfg(client_id=client_id, port=PORT, broker=BROKER, username=USERNAME, password=PASSWORD)
follower_volt_publisher = connect_client(clientCfg=clientCfg)

leader_volt_topic = "leader/volt"
client_id = 'leader_volt_publisher'
clientCfg = ClientCfg(client_id=client_id, port=PORT, broker=BROKER, username=USERNAME, password=PASSWORD)
leader_volt_publisher = connect_client(clientCfg=clientCfg)



def teleop_loop(
    teleop: Teleoperator, robot: Robot, fps: int, display_data: bool = False, duration: float | None = None
):
    
    start = time.perf_counter()

    while True:
        loop_start = time.perf_counter()
        action = teleop.get_action()

        robot.send_action(action)
        dt_s = time.perf_counter() - loop_start

        leader_pos = teleop.get_action()
        follower_pos = robot.get_observation()

        leader_temp = teleop.get_temperature()
        follower_temp = robot.get_temperature()

        leader_volt = teleop.get_voltage()
        follower_volt = robot.get_voltage()

        publish(leader_pos_publisher, leader_pos_topic, leader_pos)
        publish(follower_pos_publisher, follower_pos_topic, follower_pos)

        publish(leader_temp_publisher, leader_temp_topic, leader_temp)
        publish(follower_temp_publisher, follower_temp_topic, follower_temp)

        publish(leader_volt_publisher, leader_volt_topic, leader_volt)
        publish(follower_volt_publisher, follower_volt_topic, follower_volt)

        busy_wait(1 / fps - dt_s)

        loop_s = time.perf_counter() - loop_start
        
        print(f"\ntime: {loop_s * 1e3:.2f}ms ({1 / loop_s:.0f} Hz)")

        if duration is not None and time.perf_counter() - start >= duration:
            return



@draccus.wrap()
def teleoperate(cfg: TeleoperateConfig):

    init_logging()

    teleop = make_teleoperator_from_config(cfg.teleop)
    robot = make_robot_from_config(cfg.robot)

    teleop.connect()
    robot.connect()

    print("CONNECTED", flush=True)
 
    set_rest_pose(teleop=teleop, robot=robot, rest_pose=REST_POSE, fps=cfg.fps)

    print("READY", flush=True)

    try:
        teleop_loop(teleop, robot, cfg.fps, display_data=cfg.display_data, duration=cfg.teleop_time_s)
    except KeyboardInterrupt:
        pass





if __name__ == "__main__":
    teleoperate()

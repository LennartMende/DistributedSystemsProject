"""
```
shell
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
from lerobot.utils import ClientCfg, publish
from lerobot.utils import connect as connect_client
from lerobot.motor_read_write import set_rest_pose

# the following imports are not neccesary for the script itself, but for shell command and argument parsing via draccus
from lerobot.common.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.common.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig



print("Start of teleop script")

@dataclass
class TeleoperateConfig:
    teleop: TeleoperatorConfig
    robot: RobotConfig
    fps: int = 60
    teleop_time_s: float | None = None
    display_data: bool = False


mqtt_active = False

try:
    # create clients
    publishers = []
    # positions
    print("Before follower_pos_topic = 'follower/pos'")
    follower_pos_topic = "follower/pos"
    print("After follower_pos_topic = 'follower/pos'")
    client_id = 'follower_pos_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    print("After clientCfg = ClientCfg(client_id=client_id)")
    follower_pos_publisher = connect_client(clientCfg=clientCfg)
    print("follower_pos_publisher = connect_client(clientCfg=clientCfg)")
    publishers.append(follower_pos_publisher)
    print("After follower_pos_publisher")

    leader_pos_topic = "leader/pos"
    client_id = 'leader_pos_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    leader_pos_publisher = connect_client(clientCfg=clientCfg)
    publishers.append(leader_pos_publisher)
    print("After leader_pos_publisher")

    # temperatures
    follower_temp_topic = "follower/temp"
    client_id = 'follower_temp_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    follower_temp_publisher = connect_client(clientCfg=clientCfg)
    publishers.append(follower_temp_publisher)
    print("After follower_temp_publisher")

    leader_temp_topic = "leader/temp"
    client_id = 'leader_temp_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    leader_temp_publisher = connect_client(clientCfg=clientCfg)
    publishers.append(leader_temp_publisher)

    # voltages
    follower_volt_topic = "follower/volt"
    client_id = 'follower_volt_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    follower_volt_publisher = connect_client(clientCfg=clientCfg)
    publishers.append(follower_volt_publisher)

    print("After follower_volt_publisher")

    leader_volt_topic = "leader/volt"
    client_id = 'leader_volt_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    leader_volt_publisher = connect_client(clientCfg=clientCfg)
    publishers.append(leader_volt_publisher)
    print("After leader_volt_publisher")

    # state
    system_state_topic = "system/state"
    client_id = 'system_state_publisher'
    clientCfg = ClientCfg(client_id=client_id)
    print("After system_state_publisher init, before system_state_publisher connection")
    system_state_publisher = connect_client(clientCfg=clientCfg)
    publishers.append(system_state_publisher)

    print("After system_state_publisher")

    for publisher in publishers:
        publisher.loop_start()

    mqtt_active = True
    

except Exception:
    mqtt_active = False

finally:
    print("mqtt_active = ", mqtt_active)



def teleop_loop(
    teleop: Teleoperator, robot: Robot, fps: int, display_data: bool = False, duration: float | None = None
):
    start_time = time.perf_counter()

    while True:
        loop_start = time.perf_counter()
        action = teleop.get_action()

        robot.send_action(action)
        dt_s = time.perf_counter() - loop_start

        if mqtt_active:
            leader_pos = teleop.get_action()
            follower_pos = robot.get_observation()

            leader_temp = teleop.get_temperature()
            follower_temp = robot.get_temperature()

            leader_volt = teleop.get_voltage()
            follower_volt = robot.get_voltage()

            publish(client=leader_pos_publisher, topic=leader_pos_topic, data=leader_pos, start_time=start_time)
            publish(client=follower_pos_publisher, topic=follower_pos_topic, data=follower_pos, start_time=start_time)

#            publish(client=leader_temp_publisher, topic=leader_temp_topic, data=leader_temp, start_time=start_time)
 #           publish(client=follower_temp_publisher, topic=follower_temp_topic, data=follower_temp, start_time=start_time)

  #          publish(client=leader_volt_publisher, topic=leader_volt_topic, data=leader_volt, start_time=start_time)
   #         publish(client=follower_volt_publisher, topic=follower_volt_topic, data=follower_volt, start_time=start_time)

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

    if mqtt_active:
        publish(client=system_state_publisher, topic=system_state_topic, data={"state" : "RESETTING"}, start_time=time.perf_counter())
 
    set_rest_pose(teleop=teleop, robot=robot, rest_pose=REST_POSE, fps=cfg.fps)

    print("READY", flush=True)
    if mqtt_active:
        publish(client=system_state_publisher, topic=system_state_topic, data={"state" : "RUNNING"}, start_time=time.perf_counter())
    try:
        teleop_loop(teleop, robot, cfg.fps, display_data=cfg.display_data, duration=cfg.teleop_time_s)
    except KeyboardInterrupt:
        pass





if __name__ == "__main__":
    teleoperate()


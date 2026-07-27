"""
```shell    
python3 -m lerobot.motor_read_write --robot.type=so101_follower --robot.port=/dev/so-follower --robot.id=my_follower --teleop.type=so101_leader --teleop.port=/dev/so-leader --teleop.id=my_leader
```
"""

import sys
import time
import logging
import draccus

from dataclasses import dataclass

from lerobot.common.robots import Robot, RobotConfig, make_robot_from_config
from lerobot.common.teleoperators import Teleoperator, TeleoperatorConfig, make_teleoperator_from_config
from lerobot.common.utils.robot_utils import busy_wait
from lerobot.common.utils.utils import init_logging
from lerobot.common.errors import DeviceNotConnectedError

from lerobot.constants import REST_POSE

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



def check_connection(cfg: TeleoperateConfig):

    try:
        teleop = make_teleoperator_from_config(cfg.teleop)
        robot = make_robot_from_config(cfg.robot)

        teleop.connect()
        robot.connect()

        return True, teleop, robot

    except Exception as e:
        logger.warning(f"Connection failed: {e}")
        return False, None, None



def read_test_leader(teleop: Teleoperator):

    print("Read test on the teleoperator:")

    action = teleop.bus.sync_read("Present_Position")

    for motor, val in action.items():
        logger.debug({f"{motor}.pos": val}, "Leader OK")



def read_test_follower(robot: Robot):

    if not robot.is_connected:
        raise DeviceNotConnectedError(f"{robot} is not connected.")

    obs_dict = robot.bus.sync_read("Present_Position")

    for motor, val in obs_dict.items():
        logger.debug({f"{motor}.pos": val}, "Follower OK")



def set_rest_pose(
    teleop: Teleoperator,
    robot: Robot,
    rest_pose: dict,
    fps: int,
    duration: float | None = 3,
):
    
    from lerobot.record_and_replay import Progress
    
    start = time.perf_counter()
    progress = Progress(duration=duration, start=start, prev_remaining=None, event="resetting")

    while True:
        loop_start = time.perf_counter()

        action = rest_pose
        robot.send_action(action)

        dt_s = time.perf_counter() - loop_start
        busy_wait(1 / fps - dt_s)

        if duration is not None and time.perf_counter() - start >= duration:
            return
        
        else:
            progress.log_in_loop()
        


logger = logging.getLogger(__name__)

@draccus.wrap()
def read_and_set_rest_pose(cfg: TeleoperateConfig):

    init_logging()

    teleop = None
    robot = None

    try:
        success, teleop, robot = check_connection(cfg)

        if not success:
            logger.error("Connection failed")
            return False

        read_test_leader(teleop)
        read_test_follower(robot)

        set_rest_pose(
            teleop,
            robot,
            REST_POSE,
            cfg.fps,
            duration=3,
        )

        print("Read and set to rest pose successful")
        return True

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return False

    except Exception:
        logger.exception("Error during read_and_set_rest_pose")
        return False

    finally:
        if teleop:
            try:
                teleop.disconnect()
            except Exception:
                logger.warning("Failed to disconnect teleop")

        if robot:
            try:
                robot.disconnect()
            except Exception:
                logger.warning("Failed to disconnect robot")





if __name__ == "__main__":
    success = read_and_set_rest_pose()
    sys.exit(0 if success else 1)

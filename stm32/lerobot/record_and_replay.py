"""
```shell
python3 -u -m lerobot.record_and_replay --robot.type=so101_follower --robot.port=/dev/so-follower --robot.id=my_follower --teleop.type=so101_leader --teleop.port=/dev/so-leader --teleop.id=my_leader
```
"""


import json
import math
import time
import draccus

from dataclasses import dataclass

from lerobot.common.robots import Robot, RobotConfig, make_robot_from_config
from lerobot.common.teleoperators import Teleoperator, TeleoperatorConfig, make_teleoperator_from_config
from lerobot.common.utils.robot_utils import busy_wait
from lerobot.common.utils.utils import init_logging

from lerobot.constants import REST_POSE, SLEEP_DURATION, RECORD_DURATION, FPS
from lerobot.motor_read_write import set_rest_pose

# the following imports are not neccesary for the script itself, but for shell command and argument parsing via draccus
from lerobot.common.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.common.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig





@dataclass
class TeleoperateConfig:
    teleop: TeleoperatorConfig
    robot: RobotConfig
    fps: int = 60
    teleop_time_s: float | None = 20
    display_data: bool = False



dataset = []

def record_loop(
    teleop: Teleoperator, robot: Robot, fps: int = FPS, display_data: bool = False, duration: float | None = RECORD_DURATION
):
    
    start = time.perf_counter()
    progress = Progress(duration=duration, start=start, prev_remaining=None, event="recording")

    while True:
        loop_start = time.perf_counter()
        action = teleop.get_action()
        dataset.append((time.perf_counter() - start, action))

        robot.send_action(action)
        dt_s = time.perf_counter() - loop_start
        busy_wait(max(0, 1 / fps - dt_s))

        if duration is not None and time.perf_counter() - start >= duration:
            break

        if duration is not None:
            progress.log_in_loop()
    
    progress.log_after_loop()



@draccus.wrap()
def record(cfg: TeleoperateConfig):

    init_logging()

    teleop = make_teleoperator_from_config(cfg.teleop)
    robot = make_robot_from_config(cfg.robot)

    teleop.connect()
    robot.connect()

    try:
        record_loop(teleop, robot, cfg.fps, display_data=cfg.display_data, duration=cfg.teleop_time_s)
    except KeyboardInterrupt:
        pass



@draccus.wrap()
def record_with_reset(cfg: TeleoperateConfig):

    init_logging()

    teleop = make_teleoperator_from_config(cfg.teleop)
    robot = make_robot_from_config(cfg.robot)

    teleop.connect()
    robot.connect()

    set_rest_pose(
        teleop=teleop,
        robot=robot,
        rest_pose=REST_POSE,
        fps=cfg.fps
    )

    try:
        record_loop(
            teleop,
            robot,
            cfg.fps,
            display_data=cfg.display_data,
            duration=cfg.teleop_time_s
        )

    except KeyboardInterrupt:
        pass



def replay_loop_with_laps(
    robot: Robot, fps: int, dataset: list[tuple[float, dict]], duration: float | None = None
):
    
    lap = 0
    recorded_actions = [action for _, action in dataset]
    start = time.perf_counter()
    progress = Progress(duration=duration, start=start, prev_remaining=None, event="replaying")

    while True:

        loop_start = time.perf_counter()
        action = recorded_actions[lap]

        robot.send_action(action)
        dt_s = time.perf_counter() - loop_start
        busy_wait(max(0, 1 / fps - dt_s))

        if (duration is not None and time.perf_counter() - start >= duration) or (lap == len(dataset) - 1):
            break

        lap += 1
        
        if duration is not None:
            progress.log_in_loop()
        
    progress.log_after_loop()



@draccus.wrap()
def replay_with_laps(cfg: TeleoperateConfig):

    init_logging()

    robot = make_robot_from_config(cfg.robot)

    robot.connect()

    set_rest_pose(teleop=cfg.teleop, robot=robot, rest_pose=REST_POSE, fps=cfg.fps)

    try:
        replay_loop_with_laps(robot, cfg.fps, dataset=dataset, duration=cfg.teleop_time_s)
    except KeyboardInterrupt:
        pass



class Progress:
    def __init__(self, duration: float | None, start: float, prev_remaining: int | None, event: str):
        if type(duration) is None:
            raise TypeError("None is just possible because of campatibility with other classes, \
                            but that doesn't make sense for a  progress object.")
        self.duration = duration
        self.start = start
        self.prev_remaining = prev_remaining
        self.event = event
    
    def log_in_loop(self):
        try:
            self.remaining = self.duration - math.floor(time.perf_counter() - self.start)
        except:
            raise TypeError("None is just possible because of campatibility with other classes, \
                            but that doesn't make sense for a  progress object.")
        if (self.remaining != self.prev_remaining or self.prev_remaining is None) and self.remaining != 0:
            print(json.dumps({
                "event": self.event,
                "remaining": self.remaining
            }), flush=True)
        self.prev_remaining = self.remaining

    def log_after_loop(self):
        print(json.dumps({
            "event": self.event,
            "remaining": 0
        }), flush=True)

        

@draccus.wrap()
def record_and_replay_with_resets(cfg: TeleoperateConfig, duration: float | int = 3):

    teleop = make_teleoperator_from_config(cfg.teleop)
    robot = make_robot_from_config(cfg.robot)

    teleop.connect()
    robot.connect()

    record_with_reset(cfg)

    record_finished_time = time.perf_counter()

    set_rest_pose(
        teleop=teleop,
        robot=robot,
        rest_pose=REST_POSE,
        fps=cfg.fps,
        duration=duration
    )

#    progress = Progress(duration=SLEEP_DURATION, start=record_finished_time, prev_remaining=None, event="sleeping")

#    while time.perf_counter() - record_finished_time < SLEEP_DURATION:
 #       progress.log_in_loop()
  #      time.sleep(0.02)
   # progress.log_after_loop()

    try:
        replay_loop_with_laps(robot, cfg.fps, dataset=dataset, duration=cfg.teleop_time_s)
    except KeyboardInterrupt:
        pass
    print(json.dumps({
            "event": "finished"
        }), flush=True)





if __name__ == "__main__":
    record_and_replay_with_resets()

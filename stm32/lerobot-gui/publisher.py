import os
import time
import pyudev

from PyQt5.QtCore import QThread, pyqtSignal

from lerobot.motor_read_write import check_connection





class USBPublisher(QThread):

    usb_changed = pyqtSignal(bool, bool)

    def __init__(self):
        super().__init__()

        self.running = False
        self.last_state = (None, None)
        self.poll_interval = 1.0
        self.last_poll_time = 0



    def stop(self):

        self.running = False
        self.last_state = (None, None)



    def run(self):

        self.running = True

        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by("tty")

        self.emit_state()

        while self.running:
            device = monitor.poll(0.1)

            if device:
                self.emit_state()

            now = time.time()
            if now - self.last_poll_time > self.poll_interval:
                self.last_poll_time = now
                self.emit_state()



    def emit_state(self):

        leader = os.path.exists("/dev/so-leader")
        follower = os.path.exists("/dev/so-follower")

        state = (leader, follower)

        if state != self.last_state:
            self.last_state = state
            self.usb_changed.emit(leader, follower)





class ServoPublisher(QThread):

    servo_changed = pyqtSignal(bool, bool)

    def __init__(self, cfg):
        super().__init__()

        self.running = False
        self.cfg = cfg
        self.last_state = (None, None)
        self.poll_interval = 1.0
        self.last_poll_time = 0



    def stop(self):

        self.running = False
        self.last_state = (None, None)



    def run(self):

        self.running = True

        self.emit_state()

        while self.running:
            now = time.time()

            if now - self.last_poll_time > self.poll_interval:
                self.last_poll_time = now
                self.emit_state()

            time.sleep(0.05)



    def emit_state(self):

        leader = False
        follower = False

        teleop = None
        robot = None

        try:
            success, teleop, robot = check_connection(self.cfg)

            if success:
                leader = True
                follower = True

        except Exception:
            pass

        finally:
            
            try:
                if teleop:
                    teleop.disconnect()
            except:
                pass

            try:
                if robot:
                    robot.disconnect()
            except:
                pass

        state = (leader, follower)

        if state != self.last_state:

            self.last_state = state
            self.servo_changed.emit(*state)

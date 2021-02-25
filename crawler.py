import time
import logging

import utility
from device import Device
from config import ADB_PATH


class Crawler:
    def __init__(self, package: str, root_activity: str):
        self.package = package
        self.root_activity = root_activity
        self.device = Device()

    def start(self):
        logging.info("Crawler started.")
        self.go_to_root()
        self.save_layout()

    def go_to_root(self):
        utility.run_subprocess("{} shell am force-stop {}".format(ADB_PATH, self.package))
        utility.run_subprocess("{} shell am start -n {}/{} -W".format(ADB_PATH, self.package, self.root_activity))
        time.sleep(2)

    def save_layout(self):
        layout = self.device.dump_layout()
        print(layout)

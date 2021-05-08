import logging

from path import Path
from page import Page
from device import Device

from identifier import identifier_instance


class Crawler:
    def __init__(self, package: str, root_activity: str, device: Device):
        self.package = package
        self.root_activity = root_activity
        self.device = device

    def start(self) -> None:
        logging.info("Crawler started.")
        self.go_to_root()
        self.print_layout()

    def go_to_root(self) -> None:
        self.device.stop_activity(self.package)
        self.device.start_activity(self.package, self.root_activity)

    def print_layout(self) -> None:
        layout = self.device.dump_layout()
        print(layout)

    def follow_guide_path(self, guide_path: Path) -> None:
        logging.info("Follow guide path.")
        self.go_to_root()
        guide_origin_page = guide_path.get_origin_page()
        current_origin_page = self.device.dump_layout()
        if not identifier_instance.is_the_same_page(guide_origin_page, current_origin_page):
            logging.error("Origin page is not the same.")
            return
        before_page = guide_origin_page
        after_page = Page()
        for action in guide_path.action_list:
            # todo
            pass
import json
import logging

from path import Path
from page import Page
from device import Device
import identifier
import time

class Crawler:
    def __init__(self, package: str, root_activity: str, device: Device, strings_path, cluster_dir):
        self.package = package
        self.root_activity = root_activity
        self.device = device

        self.identifier_instance = identifier.Identifier(strings_path, cluster_dir)

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

    def follow_guide_path(self, guide_path: Path) -> bool:
        logging.info("Follow guide path.")
        self.go_to_root()
        guide_origin_page = guide_path.get_origin_page()
        current_page = Page(0)
        current_page.load_from_device(self.device)
        
        if not self.identifier_instance.is_the_same_page(guide_origin_page, current_page):
            logging.error("Origin page is not the same.")
            return False
        
        for action in guide_path.action_list:
            # todo
            # 先找节点，看看节点是否已经包含
            action_node = action.action_node
            result_nodes = self.identifier_instance.get_the_same_node(page_a=action.src_page, node_a=action_node, page_b=current_page)
            if len(result_nodes is None):
                logging.error("Node not found! Action content: {}".format(json.dumps(action.dump())))
                return False
            
            action_succeeded = False
            if action.content['typeString'] == "TYPE_VIEW_CLICKED":
                for n in result_nodes:
                    action_succeeded = self.device.click(n)
                    if action_succeeded:
                        break
                if not action_succeeded:
                    logging.error('Action (click) failed for all nodes')
                    return False
            elif action.content['typeString'] == "TYPE_VIEW_TEXT_CHANGED":
                text = action.content["param"]
                for n in result_nodes:
                    action_succeeded = self.device.enter_text(n, text)
                    if action_succeeded:
                        break
                if not action_succeeded:
                    logging.error('Action (enter text) failed for all nodes')
                    return False
            else:
                logging.error("Action {} not supported".format(action.content["typeString"]))
                return 
                

            # 检查到达的页面是不是预期的页面
            
            start_time = time.time()  # in ms
            WAITINT_LOADED = 5 # 超时时间
            to_dst_page = False
            while time.time() - start_time <= WAITINT_LOADED:
                current_page = Page(0)
                current_page.load_from_device(self.device)
                if not self.identifier_instance.is_the_same_page(action.dst_page, current_page):
                    continue
                to_dst_page = True
                break
            if not to_dst_page:
                logging.error("Not jump to the dst page")
                return False

        logging.info('success')
        return True

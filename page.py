import json
import logging
from node import Node
from queue import Queue

class Page:
    def __init__(self, index: int = -1):
        self.index = index
        self.content = dict()
        self.ui_root = None
        self.id_to_node_cache = dict()
        self.file_path = ""

    def load(self, file_path: str) -> None:
        with open(file_path) as file:
            self.content = json.load(file)
            self.file_path = file_path
        
        # 现在如果是uiAutomationServer仅仅返回一个窗口的数据
        # 如果是从文件中读取的话，就会多一层信息
        example_node = self.content[0] if isinstance(self.content, list) else self.content
        fake_root = {
            "@index": 0,
            "@class": "fake.root",
            "@package": example_node["@package"],
            "@content-desc": "",
            "@checkable": False, 
            "@checked": False,
            "@clickable": False,
            "@enabled": True, 
            "@focusable": False,
            "@focused": False,
            "@scrollable": False,
            "@long-clickable": False,
            "@password": False,
            "@selected": False,
            "@editable": False,
            "@accessibilityFocused": False,
            "@dismissable": False,
            "@drawingOrder": 0,
            "@bounds": example_node["@bounds"],
            "@screenBounds": example_node["@screenBounds"],
            "node": []
        }

        if isinstance(self.content, list):
            fake_root["node"].extend(self.content)
        else:
            fake_root["node"].append(self.content)
        q = Queue()
        q.put((None, fake_root))
        while not q.empty():
            queue_top = q.get()
            parent_node = queue_top[0] # type: Node
            crt_content = queue_top[1]

            crt_node = Node(0 if parent_node is None else len(parent_node.children))
            if self.ui_root is None:
                self.ui_root = crt_node
            if crt_node.index != crt_content['@index']:
                logging.warning("index not match {} vs {}".format(crt_node.index, crt_content['@index']))
            crt_node.write(parent_node, crt_content)
            if parent_node is not None:
                parent_node.add_child(crt_node)
            if "node" not in crt_content:
                continue
            if isinstance(crt_content['node'], dict):
                q.put((crt_node, crt_content['node']))
            else:
                for sub_item in crt_content['node']:
                    q.put((crt_node, sub_item))

    def dump(self) -> dict:
        return self.content

    def is_empty(self) -> bool:
        return bool(self.content)
    
    def get_node_by_id(self, raw_id: str):
        if raw_id in self.id_to_node_cache:
            return self.id_to_node_cache[raw_id]

        q = Queue()
        q.put(self.ui_root)
        while not q.empty():
            crt = q.get() # type: Node
            if crt is None:
                continue
            if crt.absolute_id == raw_id:
                self.id_to_node_cache[raw_id] = crt
                return crt
            if raw_id.startswith(crt.absolute_id):
                for c in crt.children:
                    q.put(c)
        
        self.id_to_node_cache[raw_id] = None
        return None


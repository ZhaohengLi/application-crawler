from page import Page
from node import Node
from cpp_bridge import CppBridge
import os


class Identifier:
    def __init__(self, strings_path, cluster_result):
        self.version = ""
        self.bridge = CppBridge()
        self.controller_pointer = self.bridge.load_cluster_from_file(strings_path, cluster_result)
        self.page_to_instance_pointer = dict()
        
    def get_instance_pointer_from_page(self, p: Page):
        if len(p.file_path) == 0:
            return 0
        if p in self.page_to_instance_pointer:
            return self.page_to_instance_pointer[p][0]
        
        ui_root_pointer = self.bridge.build_tree(p.file_path)
        instance_pointer = self.bridge.build_instance(ui_root_pointer, self.controller_pointer, p.file_path)
        self.page_to_instance_pointer[p] = (instance_pointer, ui_root_pointer)
        return instance_pointer
    
    def clear_page(self, p):
        if p not in self.page_to_instance_pointer:
            return
        self.bridge.clear_instance_all(self.page_to_instance_pointer[p][0])
        del self.page_to_instance_pointer[p]

    def is_the_same_page(self, page_a: Page, page_b: Page, clear_a=False, clear_b=False) -> bool:
        p_a = self.get_instance_pointer_from_page(page_a)
        p_b = self.get_instance_pointer_from_page(page_b)
        page_cluster_a = self.bridge.get_page_cluster(self.controller_pointer, p_a)
        page_cluster_b = self.bridge.get_page_cluster(self.controller_pointer, p_b)
        if clear_a:
            self.clear_page(p_a)
        if clear_b:
            self.clear_page(p_b)
        return page_cluster_a == page_cluster_b
    
    def get_page_cluster_index_from_page(self, p: Page, clear=False):
        p_p = self.get_instance_pointer_from_page(p)
        p_c = self.bridge.get_page_cluster(self.controller_pointer, p_p)
        idx = self.bridge.get_page_cluster_index(p_c) if (p_c is not None and p_c != 0) else -1
        if clear:
            self.clear_page(p_p)
        return idx

    def get_the_same_node(self, page_a: Page, node_a: Node, page_b: Page) -> Node:
        node_b = Node(0)
        return node_b


if __name__ == "__main__":
    strings_path = os.path.abspath("./strings/wechat_strings.txt")
    cluster_dir = os.path.abspath("./data/wechat001")
    identifier = Identifier(strings_path, cluster_dir)

    page_1 = Page(0)
    page_1.load("./data/wechat001/3/1610937568512_dst_layout.xml")
    idx = identifier.get_page_cluster_index_from_page(page_1)
    print(idx)



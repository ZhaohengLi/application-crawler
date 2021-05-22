import json
import logging
from shutil import which
from page import Page
from node import Node
from cpp_bridge import CppBridge
import os
from device import Device
from typing import List

class Identifier:
    def __init__(self, strings_path, cluster_result):
        self.version = ""
        self.bridge = CppBridge()
        self.controller_pointer = self.bridge.load_cluster_from_file(strings_path, cluster_result)
        self.page_to_instance_pointer = dict()
        self.page_to_cluster_pointer = dict()
        
    def get_instance_pointer_from_page(self, p: Page):
        if p in self.page_to_instance_pointer:
            return self.page_to_instance_pointer[p][0]
        
        if len(p.file_path) != 0:
            ui_root_pointer = self.bridge.build_tree(p.file_path)
        elif len(p.content_str) != 0:
            ui_root_pointer = self.bridge.build_tree_by_content(p.content_str)
        else:
            logging.warning('Page Not Loaded')
            return 0
        
        instance_pointer = self.bridge.build_instance(ui_root_pointer, self.controller_pointer, p.file_path)
        self.page_to_instance_pointer[p] = (instance_pointer, ui_root_pointer)
        return instance_pointer
    
    def clear_page(self, p: Page):
        if p not in self.page_to_instance_pointer:
            return
        self.bridge.clear_instance_all(self.page_to_instance_pointer[p][0], self.page_to_instance_pointer[p][1])
        del self.page_to_instance_pointer[p]
        if p in self.page_to_cluster_pointer:
            del self.page_to_cluster_pointer[p]

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
    
    def get_page_cluster_pointer(self, p: Page):
        if p in self.page_to_cluster_pointer:
            return self.page_to_cluster_pointer[p]
        instance_pointer = self.get_instance_pointer_from_page(p)
        p_c_p = self.bridge.get_page_cluster(self.controller_pointer, instance_pointer)
        self.page_to_cluster_pointer[p] = p_c_p
        return p_c_p
    
    def get_page_cluster_index_from_page(self, p: Page, clear=False):
        # p_p = self.get_instance_pointer_from_page(p)
        # p_c = self.bridge.get_page_cluster(self.controller_pointer, p_p)
        p_c = self.get_page_cluster_pointer(p)
        idx = self.bridge.get_page_cluster_index(p_c) if (p_c is not None and p_c != 0) else -1
        if clear:
            self.clear_page(p)
        return idx
    
    def get_node_pointer_by_id(self, p: Page, node: Node):
        instance_pointer = self.get_instance_pointer_from_page(p)
        node_id = node.absolute_id
        node_pointer = self.bridge.get_node_pointer_by_id(instance_pointer, node_id)
        return node_pointer

    def get_the_same_node(self, page_a: Page, node_a: Node, page_b: Page) -> List[Node]:
        # 确定当前node所属于的 cluster
        node_a_pointer = self.get_node_pointer_by_id(page_a, node_a)
        node_a_cluster = self.bridge.get_node_cluster_for_node(self.get_page_cluster_pointer(page_a), node_a_pointer)

        page_b_instance_pointer = self.get_instance_pointer_from_page(page_b)
        res_node_pointers = self.bridge.get_node_pointer_list_by_cluster(page_b_instance_pointer, node_a_cluster)
        if len(res_node_pointers) == 0:
            logging.warning("Node to same cluster not found")
        
        result = []
        for node_p in res_node_pointers:
            ori_id = self.bridge.get_ori_absolute_id_for_node(node_p)
            one_node_b = page_b.get_node_by_id(ori_id)
            if one_node_b is None:
                logging.warning("Node {} not found!".format(ori_id))
            else:
                result.append(one_node_b)
        return result


if __name__ == "__main__":
    page_1 = Page(0)
    # page_1.load("./data/wechat001/3/1610937568512_dst_layout.xml")
    page_1.load("./data/wechat_red_packet/1614315712494_src_layout.json")
    # interested_node = page_1.get_node_by_cond(lambda node: '@text' in node.content and node.content['@text'] == "通讯录")
    with open("./data/wechat_red_packet/1614315712494_actions.json", 'r') as f:
        action_content = json.load(f)[0]
    interested_node = page_1.get_node_by_id(action_content['targetNodeId'])
    
    strings_path = os.path.abspath("./strings/wechat_strings.txt")
    cluster_dir = os.path.abspath("./data/wechat001")
    identifier = Identifier(strings_path, cluster_dir)
    idx = identifier.get_page_cluster_index_from_page(page_1)
    print(idx)

    device = Device("")
    while True:
        crt_page = Page(0)
        crt_page.load_from_device(device)
        crt_page_cluster = identifier.get_page_cluster_pointer(crt_page)
        idx = identifier.get_page_cluster_index_from_page(crt_page)
        print(idx)

        node_list = identifier.get_the_same_node(page_1, interested_node, crt_page)
        for n in node_list:
            logging.info("getting nodes with text " + n.content['@text'])

        identifier.clear_page(crt_page_cluster)







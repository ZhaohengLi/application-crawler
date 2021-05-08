from page import Page
from node import Node


class Identifier:
    def __init__(self):
        self.version = ""

    def is_the_same_page(self, page_a: Page, page_b: Page) -> bool:
        return True

    def get_the_same_node(self, page_a: Page, node_a: Node, page_b: Page) -> Node:
        node_b = Node(0, dict())
        return node_b


identifier_instance = Identifier()

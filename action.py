import json
from logging import NullHandler
import logging
from node import Node
import typing
from page import Page


class Action:
    def __init__(self, index: int = -1):
        self.index = index
        self.content = dict()
        self.src_page = None  # type: Page
        self.dst_page = None  # type: Page
        self.action_node = None

    def load(self, file_path: str) -> None:
        with open(file_path) as file:
            self.content = json.load(file)[0]
        if self.src_page is not None:
            absolute_id = self.content['targetNodeId']
            self.action_node = self.src_page.get_node_by_id(absolute_id)
            if self.action_node is None:
                logging.warning("Action node not found")

    def add_page(self, pages: typing.Tuple[Page]) -> None:
        self.src_page = pages[0]
        self.dst_page = pages[1]
        if self.content is not None:
            absolute_id = self.content['targetNodeId']
            self.action_node = self.src_page.get_node_by_id(absolute_id)
            if self.action_node is None:
                logging.warning("Action node not found")

    def dump(self) -> dict:
        return self.content


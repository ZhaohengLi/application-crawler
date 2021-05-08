import json
from page import Page


class Action:
    def __init__(self, index: int = -1):
        self.index = index
        self.content = dict()
        self.page = Page()

    def write(self, content: dict, page: Page) -> None:
        self.content = content
        self.page = page

    def load(self, file_path: str) -> None:
        with open(file_path) as file:
            self.content = json.load(file)

    def add_page(self, page: Page) -> None:
        self.page = page

    def dump(self) -> dict:
        return self.content

    def get_target_node(self, page):
        # todo
        pass

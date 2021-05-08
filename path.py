import os
import re
import json

from page import Page
from action import Action


class Path:
    def __init__(self):
        self.origin_page = Page()

        self.action_list = list()
        self.page_list = list()

    def load(self, directory: str) -> None:
        file_list = os.listdir(directory) if os.path.exists(directory) and os.path.isdir(directory) else list()
        file_list = sorted(file_list)
        for file in file_list:
            match_result = re.match(r'(\d+)_actions\.json', file)
            if match_result:
                timestamp = match_result.group(1)

                before_page = Page()
                before_page.load(os.path.join(directory, "{}_src_layout.json".format(timestamp)))

                if self.origin_page.is_empty():
                    self.origin_page = before_page

                after_page = Page()
                after_page.load(os.path.join(directory, "{}_dst_layout.json".format(timestamp)))
                self.page_list.append(after_page)

                action = Action()
                action.load(os.path.join(directory, "{}_actions.json".format(timestamp)))
                action.add_page(before_page)
                self.action_list.append(action)

    def dump(self) -> dict:
        return dict()

    def get_origin_page(self) -> Page:
        return self.origin_page

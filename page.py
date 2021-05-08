import json


class Page:
    def __init__(self, index: int = -1):
        self.index = index
        self.content = dict()

    def load(self, file_path: str) -> None:
        with open(file_path) as file:
            self.content = json.load(file)

    def dump(self) -> dict:
        return self.content

    def is_empty(self) -> bool:
        return bool(self.content)

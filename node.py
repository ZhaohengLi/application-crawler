import json


class Node:
    def __init__(self, index: int = -1):
        self.index = index
        self.content = dict()

    def write(self, content: dict) -> None:
        self.content = content

    def dump(self) -> dict:
        return self.content

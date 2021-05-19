import json


class Node:
    def __init__(self, index: int = -1):
        self.index = index
        self.content = dict() # 包含子节点内容
        self.parent = None
        self.children = []
        self.absolute_id = ""

    def write(self, parent, content: dict) -> None:
        self.content = content
        self.parent = parent
        if self.parent is not None:
            self.absolute_id = self.parent.absolute_id + '|' + self.content['@index'] + ';' + self.content['@class']
        else:
            self.absolute_id =  self.content['@class']
    
    def add_child(self, n):
        self.children.append(n)

    def dump(self) -> dict:
        return self.content

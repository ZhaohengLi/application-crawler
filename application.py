import json
from graph import Graph
from page import Page


class Application:
    def __init__(self, app_name):  # 初始化
        """
        :param app_name:string
        """
        self.name = app_name
        self.graph = Graph()
        self.root_page = None
        self.page_num = 0

    def init_page(self, page):  # 设定根页面
        """
        :param page: Page
        """
        self.root_page = page

    def get_path(self, tail):  # 给定一个页面找到从根页面到该页面的跳转路径
        """
        :param tail: Page
        :return: 当未设定根页面时为None 否则为[]
        """
        if self.root_page is None:
            print("No root page")
            return None
        else:
            return self.graph.get_path(self.root_page.name, tail)

    def read_json(self, json_file):
        with open(json_file, 'r', encoding='utf8') as f:
            data = json.load(f)
            f.close()
        self.crate_pages(data)

    def crate_pages(self, data, parent=None):
        if not type(data).__name__ == 'list':
            data = [data]

        for it in data:
            page = Page(self.page_num)
            self.page_num += 1
            page.info = it
            self.graph.add_node(page)
            if parent is not None:
                self.graph.add_edge(parent, page.id)
            if "node" in it:
                self.crate_pages(it["node"], page.id)


application = Application("APP")  # 我的理解Application应该是单例的


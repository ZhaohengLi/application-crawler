import graph


class Application:
    def __init__(self, app_name):  # 初始化
        """
        :param app_name:string
        """
        self.name = app_name
        self.graph = graph.Graph()
        self.root_page = None

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


application = Application("APP")  # 我的理解Application应该是单例的

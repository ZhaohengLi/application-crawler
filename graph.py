class Node:
    def __init__(self, page):  # 初始化
        """
        :param page: Page
        """
        self.page = page
        self.neighbors = {}

    def get_key(self):  # 返回此节点的页面
        """
        :return: Page
        """
        return self.page

    def add_neighbor(self, neighbor, edge_type):  # 添加邻居节点 记录操作类型 允许多种类型
        """
        :param neighbor: String
        :param edge_type: String
        :return: []
        """
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = []
        self.neighbors[neighbor].append(edge_type)

    def get_neighbors(self):  # 得到邻居页面列表
        """
        :return: []
        """
        return self.neighbors.keys()

    def get_connectType(self, neighbor):  # 返回到达一个邻居页面的操作方式
        """
        :param neighbor:
        :return:
        """
        return self.neighbors[neighbor]


# class Queue:
#     def __init__(self):  # 初始化
#         self.holder = []
#
#     def enqueue(self, val):  # 将元素push入队列
#         """
#         :param val: 元素
#         """
#         self.holder.append(val)
#
#     def dequeue(self):  # 从队首弹出一个元素
#         """
#         :return: 队列为空则None 否则为元素
#         """
#         if len(self.holder) == 0:
#             return None
#         val = self.holder[0]
#         if len(self.holder) == 1:
#             self.holder = []
#         else:
#             self.holder = self.holder[1:]
#         return val
#
#     def empty(self):  # 队列是否为空
#         """
#         :return: Boolean
#         """
#         if len(self.holder) == 0:
#             return True
#         return False


class Graph:
    def __init__(self):  # 初始化
        self.node_list = {}
        self.node_num = 0

    def add_node(self, page):  # 添加节点
        """
        :param page: Page
        """
        new_node = Node(page)
        self.node_list[page.id] = new_node
        self.node_num += 1

    def get_node(self, page_id):  # 获取节点
        """
        :param page_id: String
        :return: 节点在图中则为Node 否则None
        """
        if page_id in self.node_list:
            return self.node_list[page_id]
        else:
            return None

    def add_edge(self, head, tail, edge_type="unknown"):  # 添加边
        """
        :param head: String
        :param tail: String
        :param edge_type: String
        :return: Boolean
        """
        if (head not in self.node_list) or (tail not in self.node_list):
            return False
        self.node_list[head].add_neighbor(tail, edge_type)
        return True

    def get_path(self, head, tail, path=None):  # 获取两点之间路径
        if path is None:
            path = []
        path = path + [head]
        if head == tail:
            return path

        res_path = []
        for node in self.node_list[head].get_neighbors():
            if node not in path:
                new_path = self.get_path(node, tail, path)
                if new_path:
                    if not res_path or len(new_path) < len(res_path):
                        res_path = new_path
        return res_path

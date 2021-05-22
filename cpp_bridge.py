import ctypes
from os import set_blocking
from page import Page
def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class CppBridge():
    def __init__(self) -> None:
        self.lib = ctypes.cdll.LoadLibrary('./AccessibilityLib.so')
        self.lib.mainForNodeCluster.restype = ctypes.c_void_p
        self.lib.mainForNodeCluster.argtypes = (ctypes.c_char_p, ctypes.c_char_p)

        self.lib.buildTreeByFilePath.restype = ctypes.c_void_p
        self.lib.buildTreeByFilePath.argtypes = (ctypes.c_char_p,)

        self.lib.createInstanceWithCon.restype = ctypes.c_void_p
        self.lib.createInstanceWithCon.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p)

        self.lib.getPageClusterFromInstance.restype = ctypes.c_void_p
        self.lib.getPageClusterFromInstance.argtypes = (ctypes.c_void_p, ctypes.c_void_p)

        self.lib.getPageClusterIndex.restype = ctypes.c_int
        self.lib.getPageClusterIndex.argtypes = (ctypes.c_void_p,)

        self.lib.buildTreeByFileContent.restype = ctypes.c_void_p
        self.lib.buildTreeByFileContent.argtypes = (ctypes.c_void_p, )

        self.lib.deleteRoot.argtypes = (ctypes.c_void_p, )
        self.lib.deletePageInstance.argtypes = (ctypes.c_void_p, )

        self.lib.getNodePointerById.restype = ctypes.c_void_p
        self.lib.getNodePointerById.argtypes = (ctypes.c_void_p, ctypes.c_char_p)

        self.lib.getNodeClusterByNode.restype = ctypes.c_void_p
        self.lib.getNodeClusterByNode.argtypes = (ctypes.c_void_p, ctypes.c_void_p)

        self.lib.getNodeByCluster.restype = ctypes.POINTER(ctypes.c_void_p)
        self.lib.getNodeByCluster.argtypes = (ctypes.c_void_p, ctypes.c_void_p)

        self.lib.deleteNodeArray.argtypes = (ctypes.POINTER(ctypes.c_void_p), )

        self.lib.getCharPointerValueForNode.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
        self.lib.getCharPointerValueForNode.restype = ctypes.c_char_p

    def load_cluster_from_file(self, strings_path, cluster_result):
        return self.lib.mainForNodeCluster(bytes(strings_path, 'utf-8'), bytes(cluster_result, 'utf-8'))
    
    def build_tree(self, layout_path):
        return self.lib.buildTreeByFilePath(bytes(layout_path, 'utf-8'))
    
    def build_tree_by_content(self, content):
        return self.lib.buildTreeByFileContent(bytes(content, 'utf-8'))
    
    def build_instance(self, ui_node_pointer, controller_pointer, layout_path):
        return self.lib.createInstanceWithCon(ui_node_pointer, controller_pointer, bytes(layout_path, 'utf-8'), bytes("", 'utf-8'))
    
    def clear_instance_all(self, instance_pointer, ui_root_pointer):
        # free memory
        self.lib.deleteRoot(ui_root_pointer)
        self.lib.deletePageInstance(instance_pointer)

    def get_page_cluster(self, con_pointer, instance_pointer):
        return self.lib.getPageClusterFromInstance(con_pointer, instance_pointer)
    
    def get_page_cluster_index(self, page_cluster_pointer):
        return self.lib.getPageClusterIndex(page_cluster_pointer)

    def get_node_pointer_by_id(self, instance_pointer, absolute_id):
        return self.lib.getNodePointerById(instance_pointer, bytes(absolute_id, 'utf-8'))

    def get_node_cluster_for_node(self, page_cluster_pointer, node_pointer):
        return self.lib.getNodeClusterByNode(page_cluster_pointer, node_pointer)

    def get_node_pointer_list_by_cluster(self, page_instance_cluster_pointer, node_cluster_pointer):
        result:ctypes.POINTER(ctypes.c_void_p) = self.lib.getNodeByCluster(page_instance_cluster_pointer, node_cluster_pointer)
        count = 0
        node_pointers = []
        while True:
            if result[count] is not None:
                node_pointers.append(result[count])
                count += 1
            else:
                break
        self.lib.deleteNodeArray(result)
        return node_pointers

    def get_ori_absolute_id_for_node(self, node_pointer):
        result = self.lib.getCharPointerValueForNode(node_pointer, bytes("getOriAbsoluteId", "utf-8"))
        return result.decode('utf-8')
        
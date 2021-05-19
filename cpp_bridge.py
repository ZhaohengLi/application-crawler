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

    def load_cluster_from_file(self, strings_path, cluster_result):
        return self.lib.mainForNodeCluster(bytes(strings_path, 'utf-8'), bytes(cluster_result, 'utf-8'))
    
    def build_tree(self, layout_path):
        return self.lib.buildTreeByFilePath(bytes(layout_path, 'utf-8'))
    
    def build_instance(self, ui_node_pointer, controller_pointer, layout_path):
        return self.lib.createInstanceWithCon(ui_node_pointer, controller_pointer, bytes(layout_path, 'utf-8'), bytes("", 'utf-8'))
    
    def clear_instance_all(self, instance_pointer):
        # free memory
        pass

    def get_page_cluster(self, con_pointer, instance_pointer):
        return self.lib.getPageClusterFromInstance(con_pointer, instance_pointer)
    
    def get_page_cluster_index(self, page_cluster_pointer):
        return self.lib.getPageClusterIndex(page_cluster_pointer)
    
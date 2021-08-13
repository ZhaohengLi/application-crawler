from os.path import split
import socket
import logging
import time
import node

from config import *
import utility


class Device:
    RES_SUCCESS = "Success"
    RES_FAILED = "Failed"
    RES_NOT_FOUND = "NotFound"
    RES_ERROR_RESPONSE = "ErrorResponse"
    RES_ERROR_FORMAT = "ErrorFormat"
    RES_TIMEOUT = "Timeout"

    GLOBAL_BACK = "GlobalBack"

    def __init__(self, serial: str):
        self.serial = serial
        self.socket = None
        self.connect()

    def connect(self) -> None:
        utility.set_port_forward()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", PC_PORT))
        logging.info("Device connected.")

    def stop_activity(self, package: str) -> None:
        utility.run_subprocess("{} -s {} shell am force-stop {}".format(ADB_PATH, self.serial, package))

    def start_activity(self, package: str, activity: str) -> None:
        utility.run_subprocess("{} -s {} shell am start -n {}/{} -W".format(ADB_PATH, self.serial, package, activity))
        time.sleep(2)

    def dump_layout(self) -> str:
        self.socket.send("DUMP_LAYOUT_JSON\n".encode(TERMINAL_ENCODING))
        msg = self.socket.makefile(encoding=TERMINAL_ENCODING).readline()
        try:
            # handle '#' in content
            response_id_sep_idx = msg.index("#")
            response_id = msg[0: response_id_sep_idx]
            remain = msg[response_id_sep_idx + 1:]
            if response_id != "RES-DUMP_LAYOUT":
                raise ValueError()
            state_sep_idx = remain.index("#")
            state = remain[0: state_sep_idx]
            remain2 = remain[state_sep_idx + 1:]
            if state != Device.RES_SUCCESS:
                raise ValueError()
            return remain2
        except ValueError:
            logging.error("Dump layout\n{}".format(msg))
            return ""
            
    def click(self, n: node.Node):
        absolute_id = n.absolute_id
        self.socket.send("ACTION-CLICK#{}\n".format(absolute_id).encode(TERMINAL_ENCODING))
        msg = self.socket.makefile(encoding=TERMINAL_ENCODING).readline()
        split_res = msg.split('#')
        if len(split_res) != 2 or split_res[0] != "RES-CLICK":
            logging.warning('Invalid response {}'.format(msg))
            return False
        if split_res[1] != "Success\n":
            logging.warning('Click failed {}'.format(msg))
            return False
        return True
    
    def clear_text(self, n: node.Node):
        absolute_id = n.absolute_id
        self.socket.send("ACTION-CLEAR_TEXT#{}\n".format(absolute_id).encode(TERMINAL_ENCODING))
        msg = self.socket.makefile(encoding=TERMINAL_ENCODING).readline()
        split_res = msg.split('#')
        if len(split_res) != 2 or split_res[0] != "RES-CLEAR_TEXT":
            logging.warning('Invalid response {}'.format(msg))
            return False
        if split_res[1] != "Success\n":
            logging.warning('Clear text failed {}'.format(msg))
            return False
        return True
    
    def enter_text(self, n: node.Node, text: str):
        if text is None or len(text) == 0:
            return self.clear_text(n)
        absolute_id = n.absolute_id
        self.socket.send("ACTION-ENTER_TEXT#{}#{}\n".format(absolute_id, text).encode(TERMINAL_ENCODING))
        msg = self.socket.makefile(encoding=TERMINAL_ENCODING).readline()
        split_res = msg.split('#')
        if len(split_res) != 2 or split_res[0] != "RES-ENTER_TEXT":
            logging.warning('Invalid response {}'.format(msg))
            return False
        if split_res[1] != "Success\n":
            logging.warning('Clear text failed {}'.format(msg))
            return False
        return True


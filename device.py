import socket
import logging

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

    def __init__(self):
        utility.set_port_forward()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", PC_PORT))
        logging.info("Device connected.")

    def dump_layout(self):
        self.socket.send("DUMP_LAYOUT\n".encode(TERMINAL_ENCODING))
        msg = self.socket.makefile(encoding=TERMINAL_ENCODING).readline()
        result = msg.split("#")
        if len(result) == 3 and result[0] == "RES-DUMP_LAYOUT" and result[1] == Device.RES_SUCCESS:
            return result[2]
        else:
            logging.error("Dump layout\n{}".format(msg))
            return ""

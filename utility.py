import subprocess
import logging

from config import *


def set_port_forward():
    cmd = "{} forward tcp:{} tcp:{}".format(ADB_PATH, PC_PORT, PHONE_PORT)
    run_subprocess(cmd)


def run_subprocess(cmd: str):
    ret = subprocess.run(cmd, shell=True, capture_output=True)
    log_msg = "{}\n".format(cmd)
    if ret.returncode == 0:
        log_msg += "stdout:\n{}".format(ret.stdout.decode(TERMINAL_ENCODING))
    else:
        log_msg += "stderr:\n{}".format(ret.stderr.decode(TERMINAL_ENCODING))
    logging.info(log_msg)

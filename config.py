import shutil
TERMINAL_ENCODING = "utf8"

TEMP_FOLDER_PATH = "./temp/"
LOG_FOLDER_PATH = "./log/"
CRAWLER_LOG_FILE_PATH = LOG_FOLDER_PATH + "crawler.log"

ADB_PATH = shutil.which('adb')
if ADB_PATH is None:
    ADB_PATH = 'adb'

PC_PORT = 10001
PHONE_PORT = 10086

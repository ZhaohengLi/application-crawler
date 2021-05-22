import logging

from config import CRAWLER_LOG_FILE_PATH
from crawler import Crawler
from device import Device
from path import Path

package = "com.tencent.mm"
root_activity = "com.tencent.mm.ui.LauncherUI"
guide_directory = ""
device_serial = ""
strings_path = "" # os.path.abspath("./strings/wechat_strings.txt")
cluster_dir = "" # os.path.abspath("./data/wechat001")

logging.basicConfig(level=logging.DEBUG,
                    filename=CRAWLER_LOG_FILE_PATH,
                    datefmt='%m-%d %H:%M:%S',
                    format='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] - %(message)s')

if __name__ == "__main__":
    logging.info("Program started.")

    device = Device(device_serial)
    crawler = Crawler(package, root_activity, device, strings_path, cluster_dir)

    guide_path = Path()
    guide_path.load(guide_directory)
    crawler.follow_guide_path(guide_path)

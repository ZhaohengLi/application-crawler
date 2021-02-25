import logging

from config import CRAWLER_LOG_FILE_PATH
from crawler import Crawler

package = "com.tencent.mm"
root_activity = "com.tencent.mm.ui.LauncherUI"

logging.basicConfig(level=logging.DEBUG,
                    filename=CRAWLER_LOG_FILE_PATH,
                    datefmt='%m-%d %H:%M:%S',
                    format='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] - %(message)s')

if __name__ == "__main__":
    logging.info("Program started.")
    crawler = Crawler(package, root_activity)
    crawler.start()

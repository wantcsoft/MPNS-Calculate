import logging
import time

time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
file_name = "./logs/" + time + "-error.logs"
logging.basicConfig(filename=file_name,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pass

import os
import logging

import colorlog

from common.utils.process_time import ProcessTime
from common.path import TEST_LOG_PATH, DB_LOG_PATH, HTTP_LOG_PATH


class Log:
    """
    指定保存日志的文件路径，日志级别，以及调用文件
    将日志存入到指定的文件中
    """

    __TEST_LOG_PATH = os.path.join(TEST_LOG_PATH, ProcessTime.current_str_time("%Y_%m_%d_%H_%M_%S") + ".log")
    __DB_LOG_PATH = os.path.join(DB_LOG_PATH, ProcessTime.current_str_time("%Y_%m_%d_%H_%M_%S") + ".log")
    __HTTP_LOG_PATH = os.path.join(HTTP_LOG_PATH, ProcessTime.current_str_time("%Y_%m_%d_%H_%M_%S") + ".log")
    __LOG_COLOR_CONFIG = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }

    def __init__(self, description: str, print_to_file=False, log_path_type="test"):
        self.description = description
        if log_path_type == "test":
            self.log_path = self.__TEST_LOG_PATH
        elif log_path_type == "db":
            self.log_path = self.__DB_LOG_PATH
        elif log_path_type == "http":
            self.log_path = self.__HTTP_LOG_PATH

        self.logger = logging.getLogger(self.description)

        if self.logger.level != logging.DEBUG:
            self.logger.setLevel(logging.DEBUG)

        if self.logger.handlers:
            self.logger.handlers.clear()

        if not self.logger.handlers:
            stream_log = logging.StreamHandler()
            stream_log.setLevel(logging.DEBUG)
            self.formatter_stream = colorlog.ColoredFormatter('%(log_color)s %(asctime)s - %(name)s'
                                                              ' -> %(message)s', log_colors=self.__LOG_COLOR_CONFIG)
            stream_log.setFormatter(self.formatter_stream)
            self.logger.addHandler(stream_log)

        if print_to_file:
            file_log = logging.FileHandler(self.log_path, encoding='utf-8')
            file_log.setLevel(logging.DEBUG)
            self.formatter_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_log.setFormatter(self.formatter_file)
            self.logger.addHandler(file_log)

    @property
    def log(self):
        return self.logger

    @staticmethod
    def log_typing():
        return logging.Logger

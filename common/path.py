import os
import sys


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_CONFIG_PATH = os.path.join(ROOT_PATH, "config", "db.ini")

HTTP_CONFIG_PATH = os.path.join(ROOT_PATH, "config", "http.ini")

DB_LOG_PATH = os.path.join(ROOT_PATH, "config", "logs", "db")

HTTP_LOG_PATH = os.path.join(ROOT_PATH, "config", "logs", "http")

TEST_LOG_PATH = os.path.join(ROOT_PATH, "config", "logs", "test")

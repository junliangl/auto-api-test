import os
from abc import abstractmethod


class InitDbConfig:

    mock_url = None

    def __init__(self, environment: str):
        self.environment = environment
        os.environ["CURRENT_ENV"] = environment

    def set_mock_url(self):
        if self.environment == "local":
            self.mock_url = "http://127.0.0.1:5000"
        elif self.environment == "docker":
            self.mock_url = "http://172.18.0.1:5000"

    @abstractmethod
    def init_db(self):
        pass

import socket
from urllib.parse import urlparse

import requests

from common.utils.config import config
from common.utils.data.json import ProcessJson


class HttpService:
    """
    封装的 get, post 请求,
    """
    __PROTOCOL = None
    __HOST = None
    __PORT = None
    __URL = None

    __DEFAULT_HEADERS = {
        "content-type": "application/json"
    }

    def __init__(self, protocol=None, host=None, port=None):
        if protocol is None:
            self.__PROTOCOL = config.http_protocol
        if host is None:
            self.__HOST = config.http_host
        if port is None:
            self.__PORT = config.http_port
        self._REQUEST = requests.Session()

    @property
    def protocol(self):
        return self.__PROTOCOL

    @protocol.setter
    def protocol(self, _protocol):
        self.__PROTOCOL = _protocol

    @property
    def host(self):
        return self.__HOST

    @host.setter
    def host(self, _host):
        self.__HOST = _host

    @property
    def port(self):
        return self.__PORT

    @port.setter
    def port(self, _port):
        self.__PORT = _port

    @property
    def url(self):
        return self.__URL

    @url.setter
    def url(self, path):
        self.__URL = self.protocol + "://" + self.host + ":" + self.port + path

    @property
    def default_headers(self):
        return self.__DEFAULT_HEADERS

    @default_headers.setter
    def default_headers(self, _default_headers):
        self.__DEFAULT_HEADERS = _default_headers

    def get(self, path, headers=None, data=None, params=None, *args, **kwargs):
        self.url = path
        return self._REQUEST.get(url=self.url, headers=headers, data=data, params=params, *args, **kwargs)

    def post(self, path, headers=None, data=None, params=None, *args, **kwargs):
        self.url = path
        if kwargs.get("files", -1) != -1:
            # 如果是文件流就不处理 data
            json_ = data
        else:
            json_ = ProcessJson.obj_to_json(data)
        return self._REQUEST.post(url=self.url, headers=headers, data=json_, params=params, *args, **kwargs)

    def put(self, path, headers=None, data=None, params=None, *args, **kwargs):
        self.url = path
        json_ = ProcessJson.obj_to_json(data)
        return self._REQUEST.put(url=self.url, headers=headers, data=json_, params=params, *args, **kwargs)

    def delete(self, path, headers=None, params=None, *args, **kwargs):
        self.url = path
        return self._REQUEST.delete(url=self.url, headers=headers, params=params, *args, **kwargs)

    def patch(self, path, headers, data=None, *args, **kwargs):
        self.url = path
        json_ = ProcessJson.obj_to_json(data)
        return self._REQUEST.patch(url=self.url, headers=headers, data=json_, *args, **kwargs)

    def options(self, path, headers, *args, **kwargs):
        self.url = path
        return self._REQUEST.options(url=self.url, headers=headers, *args, **kwargs)

    def head(self, path, headers, *args, **kwargs):
        self.url = path
        return self._REQUEST.head(url=self.url, headers=headers, *args, **kwargs)

    def close(self):
        self._REQUEST.close()

    @staticmethod
    def get_ip(url):
        """
        获取 url 的 ip 地址
        """
        return urlparse(url).hostname

    @staticmethod
    def get_port(url):
        """
        获取 url 的端口号
        """
        return urlparse(url).port

    @property
    def hostname(self):
        """
        获取主机名
        """

        return socket.gethostname()

    @staticmethod
    def get_ip_by_hostname(hostname=socket.gethostname()):
        """
        通过主机名获取 ip 地址
        """

        return socket.gethostbyname(hostname)

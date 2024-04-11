import abc
import requests

from decorator.log_decorator import log_decorator

class Crawler(abc.ABC):

    def __init__(self):
        super().__init__()

    @log_decorator
    def request(self, url: str, method: str) -> requests.Response:
        return requests.request(method, url)

    def get_web_driver(self):
        ...

    def close_driver(self):
        ...

from .authorization import authorization
from .request_mapping import RequestMapping

set_header = authorization.header
HeaderType = authorization.HeaderType
url = RequestMapping.url
class_mapping = RequestMapping.class_mapping
method_mapping = RequestMapping.method_mapping

__all__ = [
    "set_header",
    "HeaderType",
    "url",
    "class_mapping",
    "method_mapping",
]

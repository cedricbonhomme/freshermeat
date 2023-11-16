import logging
import types
import urllib

from flask import request
from flask import url_for

logger = logging.getLogger(__name__)


def default_handler(obj, role="admin"):
    """JSON handler for default query formatting"""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if hasattr(obj, "dump"):
        return obj.dump(role=role)
    if isinstance(obj, (set, frozenset, types.GeneratorType)):
        return list(obj)
    if isinstance(obj, BaseException):
        return str(obj)
    raise TypeError(
        "Object of type %s with value of %r "
        "is not JSON serializable" % (type(obj), obj)
    )


def rebuild_url(url, base_split):
    split = urllib.parse.urlsplit(url)
    if split.scheme and split.netloc:
        return url  # url is fine
    new_split = urllib.parse.SplitResult(
        scheme=split.scheme or base_split.scheme,
        netloc=split.netloc or base_split.netloc,
        path=split.path,
        query="",
        fragment="",
    )
    return urllib.parse.urlunsplit(new_split)


def redirect_url(default="services"):
    return request.args.get("next") or request.referrer or url_for(default)

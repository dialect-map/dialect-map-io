# -*- coding: utf-8 -*-

from typing import Type
from typing import Union
from pathlib import Path
from urllib.request import Request

from .apis import *
from .files import *


BaseHandler = Union[BaseAPIHandler, BaseFileHandler]


def _get_handler_cls_for_api(uri: Request) -> Type[BaseAPIHandler]:
    """
    Returns an API handler class depending on the provided URI
    :param uri: URI to get the API handler class from
    :return: API handler class
    """

    if uri.host == "localhost":
        return RestAPIHandler
    elif uri.host == "export.arxiv.org":
        return ArxivAPIHandler
    elif uri.host.startswith("dialect-map"):
        return DialectMapAPIHandler
    else:
        raise ValueError("API handler not specified for the provided URI")


def _get_handler_cls_for_file(uri: Request) -> Type[BaseFileHandler]:
    """
    Returns a file handler class depending on the provided URI
    :param uri: URI to get the file handler class from
    :return: file handler class
    """

    extension = Path(uri.selector).suffix

    if extension == ".json":
        return JSONFileHandler
    elif extension == ".txt":
        return TextFileHandler
    elif extension == ".pdf":
        return PDFFileHandler
    else:
        raise ValueError("File handler not specified for the provided URI")


def get_handler_cls(uri: Request) -> Type[BaseHandler]:
    """
    Returns a handler class depending on the provided URI
    :param uri: URI to get the handler class from
    :return: handler class
    """

    if uri.type == "file":
        return _get_handler_cls_for_file(uri)
    elif uri.type in {"http", "https"}:
        return _get_handler_cls_for_api(uri)
    else:
        raise ValueError("Handler not specified for the provided URI")

# -*- coding: utf-8 -*-

from typing import Union
from pathlib import Path
from urllib.request import Request

from .apis import *
from .files import *


BaseHandler = Union[BaseAPIHandler, BaseFileHandler]


def _init_api_handler_cls(uri: Request, **kwargs) -> BaseAPIHandler:
    """
    Returns an API handler instance depending on the provided URI
    :param uri: URI to get the API handler instance for
    :param kwargs: additional keyword arguments to pass
    :return: API handler instance
    """

    if uri.host == "localhost":
        return RestAPIHandler(base_url=uri.full_url, **kwargs)
    elif uri.host == "export.arxiv.org":
        return ArxivAPIHandler(base_url=uri.full_url)
    elif uri.host.startswith("dialect-map"):
        return DialectMapAPIHandler(base_url=uri.full_url)
    else:
        raise ValueError("API handler not specified for the provided URI")


def _init_file_handler_cls(uri: Request, **_) -> BaseFileHandler:
    """
    Returns a file handler instance depending on the provided URI
    :param uri: URI to get the file handler instance for
    :param _: additional keyword arguments to pass
    :return: file handler instance
    """

    extension = Path(uri.selector).suffix

    if extension == ".json":
        return JSONFileHandler()
    elif extension == ".txt":
        return TextFileHandler()
    elif extension == ".pdf":
        return PDFFileHandler()
    else:
        raise ValueError("File handler not specified for the provided URI")


def init_handler_cls(uri: Request, **kwargs) -> BaseHandler:
    """
    Returns a handler instance depending on the provided URI
    :param uri: URI to get the handler instance for
    :param kwargs: additional keyword arguments to pass
    :return: handler instance
    """

    if uri.type in {"file"}:
        return _init_file_handler_cls(uri, **kwargs)
    elif uri.type in {"http", "https"}:
        return _init_api_handler_cls(uri, **kwargs)
    else:
        raise ValueError("Handler not specified for the provided URI")

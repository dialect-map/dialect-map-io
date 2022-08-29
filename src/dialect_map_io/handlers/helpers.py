# -*- coding: utf-8 -*-

from typing import Union
from pathlib import Path
from urllib.request import Request as URI

from .apis import *
from .files import *


BaseHandler = Union[BaseAPIHandler, BaseFileHandler]


def _init_api_handler_cls(uri: URI, **kwargs) -> BaseAPIHandler:
    """
    Returns an API handler instance depending on the provided URI
    :param uri: URI to get the API handler instance for
    :param kwargs: additional keyword arguments to pass
    :return: API handler instance
    """

    match uri.host:
        case "localhost":
            return RestAPIHandler(base_url=uri.full_url, **kwargs)
        case "export.arxiv.org":
            return ArxivAPIHandler(base_url=uri.full_url)
        case host if host.startswith("dialect-map"):
            return DialectMapAPIHandler(base_url=uri.full_url)

    raise ValueError("API handler not specified for the provided URI")


def _init_file_handler_cls(uri: URI, **_) -> BaseFileHandler:
    """
    Returns a file handler instance depending on the provided URI
    :param uri: URI to get the file handler instance for
    :param _: additional keyword arguments to pass
    :return: file handler instance
    """

    extension = Path(uri.selector).suffix

    match extension:
        case ".json":
            return JSONFileHandler()
        case ".txt":
            return TextFileHandler()
        case ".pdf":
            return PDFFileHandler()

    raise ValueError("File handler not specified for the provided URI")


def init_handler_cls(uri: URI, **kwargs) -> BaseHandler:
    """
    Returns a handler instance depending on the provided URI
    :param uri: URI to get the handler instance for
    :param kwargs: additional keyword arguments to pass
    :return: handler instance
    """

    match uri.type:
        case "file":
            return _init_file_handler_cls(uri, **kwargs)
        case "http" | "https":
            return _init_api_handler_cls(uri, **kwargs)

    raise ValueError("Handler not specified for the provided URI")

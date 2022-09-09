# -*- coding: utf-8 -*-

from pathlib import Path
from urllib.parse import ParseResult

from .apis import *
from .files import *


BaseHandler = BaseAPIHandler | BaseFileHandler


def _init_api_handler_cls(url: ParseResult, **kwargs) -> BaseAPIHandler:
    """
    Returns an API handler instance depending on the provided URL
    :param url: parsed URL to initialize the API handler for
    :param kwargs: additional keyword arguments to pass
    :return: API handler instance
    """

    full_url = url.geturl()

    match url.hostname:
        case "localhost":
            return RestAPIHandler(base_url=full_url, **kwargs)
        case "export.arxiv.org":
            return ArxivAPIHandler(base_url=full_url)
        case host if host and host.startswith("dialect-map"):
            return DialectMapAPIHandler(base_url=full_url)

    raise ValueError("API handler not specified for the provided URL")


def _init_file_handler_cls(url: ParseResult, **_) -> BaseFileHandler:
    """
    Returns a file handler instance depending on the provided URL
    :param url: parsed URL to initialize the file handler for
    :param _: additional keyword arguments to pass
    :return: file handler instance
    """

    extension = Path(url.path).suffix

    match extension:
        case ".json":
            return JSONFileHandler()
        case ".txt":
            return TextFileHandler()
        case ".pdf":
            return PDFFileHandler()

    raise ValueError("File handler not specified for the provided URL")


def init_handler_cls(url: ParseResult, **kwargs) -> BaseHandler:
    """
    Returns a handler instance depending on the provided URL
    :param url: parsed URL to initialize the handler for
    :param kwargs: additional keyword arguments to pass
    :return: handler instance
    """

    match url.scheme:
        case "file":
            return _init_file_handler_cls(url, **kwargs)
        case "http" | "https":
            return _init_api_handler_cls(url, **kwargs)

    raise ValueError("Handler not specified for the provided URL")

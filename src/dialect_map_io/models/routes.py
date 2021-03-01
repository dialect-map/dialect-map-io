# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class APIRoute:
    """
    Object containing the basic information for a remote API route

    :attr api_name: informative name of the API
    :attr api_path: specific path within the API base URL
    :attr model_name: specific data model associated to the route
    """

    api_name: str
    api_path: str
    model_name: str

# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class APIRoute:
    """
    Object containing the basic information for a remote API route

    :attr api_name: informative name of the API
    :attr api_route: specific route within the API base URL
    :attr model_name: specific data model associated to the route
    """

    api_name: str
    api_route: str
    model_name: str

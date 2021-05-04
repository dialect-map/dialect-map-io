# -*- coding: utf-8 -*-

from .local_files import LocalJSONFile
from .local_files import LocalPDFFile
from .local_files import LocalTXTFile

from .pubsub_gcp import PubSubReader

from .remote_apis import BaseInputAPI
from .remote_apis import ArxivInputAPI
from .remote_apis import RestInputAPI

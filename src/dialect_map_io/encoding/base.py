# -*- coding: utf-8 -*-

from typing import TypeVar


# Generic decoder data types
BaseBinaryContent = TypeVar("BaseBinaryContent", bound=object)
BasePlainContent = TypeVar("BasePlainContent", bound=object)

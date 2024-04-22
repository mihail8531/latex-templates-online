from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING, Annotated, TypeAlias
from pydantic import BaseModel, Field, AfterValidator, constr
import string


from typing import Any

from . import widgets as widgets
from .exceptions import FieldError as FieldError


class Field:
    empty_values: Any
    attribute: Any
    default: Any
    column_name: Any
    widget: Any
    readonly: Any
    saves_null_values: Any
    dehydrate_method: Any
    m2m_add: Any
    def __init__(self, attribute: Any | None = ..., column_name: Any | None = ..., widget: Any | None = ..., default: Any=..., readonly: bool = ..., saves_null_values: bool = ..., dehydrate_method: Any | None = ..., m2m_add: bool = ...) -> None: ...
    def clean(self, data: Any, **kwargs: Any) -> Any: ...
    def get_value(self, obj: Any) -> Any: ...
    def save(self, obj: Any, data: Any, is_m2m: bool = ..., **kwargs: Any) -> None: ...
    def export(self, obj: Any) -> Any: ...
    def get_dehydrate_method(self, field_name: Any | None = ...) -> Any: ...

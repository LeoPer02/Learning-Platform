from typing import Any

def format_datetime(value: Any, datetime_format: Any) -> Any: ...

class Widget:
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class NumberWidget(Widget):
    coerce_to_string: Any
    def __init__(self, coerce_to_string: bool = ...) -> None: ...
    def is_empty(self, value: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class FloatWidget(NumberWidget):
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...

class IntegerWidget(NumberWidget):
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...

class DecimalWidget(NumberWidget):
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...

class CharWidget(Widget): ...

class BooleanWidget(Widget):
    TRUE_VALUES: Any
    FALSE_VALUES: Any
    NULL_VALUES: Any
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...

class DateWidget(Widget):
    formats: Any
    def __init__(self, format: Any | None = ...) -> None: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class DateTimeWidget(Widget):
    formats: Any
    def __init__(self, format: Any | None = ...) -> None: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class TimeWidget(Widget):
    formats: Any
    def __init__(self, format: Any | None = ...) -> None: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class DurationWidget(Widget):
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class SimpleArrayWidget(Widget):
    separator: Any
    def __init__(self, separator: Any | None = ...) -> None: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class JSONWidget(Widget):
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class ForeignKeyWidget(Widget):
    model: Any
    field: Any
    use_natural_foreign_keys: Any
    def __init__(self, model: Any, field: str = ..., use_natural_foreign_keys: bool = ..., **kwargs: Any) -> None: ...
    def get_queryset(self, value: Any, row: Any, *args: Any, **kwargs: Any) -> Any: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

class ManyToManyWidget(Widget):
    model: Any
    separator: Any
    field: Any
    def __init__(self, model: Any, separator: Any | None = ..., field: Any | None = ..., **kwargs: Any) -> None: ...
    def clean(self, value: Any, row: Any | None = ..., **kwargs: Any) -> Any: ...
    def render(self, value: Any, obj: Any | None = ...) -> Any: ...

from typing import Any


class BaseInstanceLoader:
    resource: Any
    dataset: Any
    def __init__(self, resource: Any, dataset: Any | None = ...) -> None: ...
    def get_instance(self, row: Any) -> None: ...

class ModelInstanceLoader(BaseInstanceLoader):
    def get_queryset(self) -> Any: ...
    def get_instance(self, row: Any) -> Any: ...

class CachedInstanceLoader(ModelInstanceLoader):
    pk_field: Any
    all_instances: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_instance(self, row: Any) -> Any: ...

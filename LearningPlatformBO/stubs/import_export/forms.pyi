from typing import Any
from django import forms

class ImportExportFormBase(forms.Form):
    resource: Any
    def __init__(self, *args: Any, resources: Any | None = ..., **kwargs: Any) -> None: ...

class ImportForm(ImportExportFormBase):
    import_file: Any
    input_format: Any
    def __init__(self, import_formats: Any, *args: Any, **kwargs: Any) -> None: ...
    @property
    def media(self) -> Any: ...

class ConfirmImportForm(forms.Form):
    import_file_name: Any
    original_file_name: Any
    input_format: Any
    resource: Any
    def clean_import_file_name(self) -> Any: ...

class ExportForm(ImportExportFormBase):
    file_format: Any
    def __init__(self, formats: Any, *args: Any, **kwargs: Any) -> None: ...

def export_action_form_factory(formats: Any) -> Any: ...

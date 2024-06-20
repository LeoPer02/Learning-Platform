from typing import Any, Optional
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import URLPattern

class BaseOrderedModelAdmin:
    request_query_string: str
    def changelist_view(self, request: HttpRequest, extra_context: Optional[dict[str, Any]] = ...) -> HttpResponse: ...

class OrderedModelAdmin(BaseOrderedModelAdmin, admin.ModelAdmin):
    def get_urls(self) -> list[URLPattern]: ...
    def move_view(self, request: HttpRequest, object_id: str, direction: str) -> HttpResponseRedirect: ...
    def move_up_down_links(self, obj: str) -> str: ...

class OrderedInlineModelAdminMixin:
    def get_urls(self) -> list[URLPattern]: ...

class OrderedInlineMixin(BaseOrderedModelAdmin):
    def get_urls(self) -> list[URLPattern]: ...
    def move_view(
        self, request: HttpRequest, admin_id: str, object_id: str, direction: str
    ) -> HttpResponseRedirect: ...
    def move_up_down_links(self, obj: str) -> str: ...

class OrderedTabularInline(OrderedInlineMixin, admin.TabularInline): ...
class OrderedStackedInline(OrderedInlineMixin, admin.StackedInline): ...
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from core.utilities.types import URLPatternsList


urlpatterns: URLPatternsList = [
    path("", include("core.urls")),
    path("users/", include("users.urls")),
    path("course/", include("course.urls")),
    path("api/", include([
        path("", include("course.urls")),
        path("", include("topic.urls")),
    ])),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

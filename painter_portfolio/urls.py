from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    path("api/", include("gallery.urls")),
]

# React SPA Catch-All
# هر چیزی که api و static و media نباشد → index.html
urlpatterns += [
    re_path(
        r"^(?!api/|static/|media/).*",
        TemplateView.as_view(template_name="index.html"),
    ),
]

# فقط در حالت توسعه (لوکال)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
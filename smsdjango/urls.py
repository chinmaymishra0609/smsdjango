from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from user.views import UserLoginView

urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("student/", include("student.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
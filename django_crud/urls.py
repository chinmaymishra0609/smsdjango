from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from student import views as sv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include("student.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
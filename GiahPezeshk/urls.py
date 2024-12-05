from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

api_version = "v1"
urlpatterns = [
    path('admin/', admin.site.urls),
    path(f"api/{api_version}/accounts/", include("accounts.urls"))
]


# media and static files
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

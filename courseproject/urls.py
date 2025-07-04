
from django.contrib import admin
from django.urls import path, include

# To display Images
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('courses.urls')),
    path('', include('core.urls')),
    path('teachers/', include('teachers.urls')),
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout uchun

]
# To Display Images while onlocal server
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

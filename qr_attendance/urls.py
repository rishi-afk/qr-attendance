from django.contrib import admin
from django.urls import path, include, re_path
import debug_toolbar
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('scanner/', include('scanner.urls')),
    path('api/', include('api.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    re_path(r'^chaining/', include('smart_selects.urls')),
]

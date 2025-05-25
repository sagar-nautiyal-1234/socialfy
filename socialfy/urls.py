from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView  # ✅ Import LogoutView

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('social.urls')),

    # ✅ Logout using Django's built-in view
    path('logout/', LogoutView.as_view(), name='logout'),
]

# ✅ Serve media files in development mode only
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

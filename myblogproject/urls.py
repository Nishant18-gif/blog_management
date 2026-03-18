from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import home, login_frontend,logout_frontend   # frontend views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend home page
    path('', home, name='home'),

    # Frontend login
    path('login/', login_frontend, name='login_frontend'),
    path('logout/', logout_frontend, name='logout_frontend'),

    # All blog API URLs
    path('api/', include('blog.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
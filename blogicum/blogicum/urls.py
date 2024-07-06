from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
import blogicum.settings as settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'pages.views.csrf_failure'

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.internal_error'

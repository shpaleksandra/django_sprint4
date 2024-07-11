from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


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


# Роман, здравствуйте! Исправила только критические замечания,
# ибо ничего в этой жизни не успеваю, но спасибо вам большое,
# что прописываете, что можно было сделать лучше,
# правда, очень ценно

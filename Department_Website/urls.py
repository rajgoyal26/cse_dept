from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from user.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/', include('user.urls', namespace="user")),
    path('student/', include('student.urls', namespace="student")),
    path('message/', include('communication.urls', namespace='message')),
    path('faculty/', include('faculty.urls',namespace='faculty')),
    path('reach_us/', TemplateView.as_view(template_name='home/reach_us.html'), name='reach_us'),
    path('assessment/', include('assessment.urls', namespace="assessment")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


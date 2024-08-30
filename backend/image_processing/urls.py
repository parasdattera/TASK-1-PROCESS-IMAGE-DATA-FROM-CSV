from django.urls import path
from .views import UploadCSV,CheckStatus
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload_csv'),
        path('status/<str:request_id>/', CheckStatus.as_view(), name='check_status'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
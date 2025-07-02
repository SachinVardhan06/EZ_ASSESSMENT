from django.urls import path
from .views import (
    OpsLoginView,
    ClientLoginView,
    FileUploadView,
    FileListView,
    FileDownloadView,
    ClientSignupView,
    EmailVerifyView,
    FileDownloadTokenView,
    SecureFileDownloadView,
)
from . import views

urlpatterns = [
    path('ops/login/', OpsLoginView.as_view(), name='ops-login'),
    path('client/signup/', ClientSignupView.as_view(), name='client-signup'),
    path('client/login/', ClientLoginView.as_view(), name='client-login'),
    path('client/verify-email/', EmailVerifyView.as_view(), name='verify-email'),
    path('ops/upload/', FileUploadView.as_view(), name='file-upload'),
    path('client/files/', FileListView.as_view(), name='file-list'),
    path('frontend/', views.frontend, name='frontend'),

    # Distinct endpoints for file info and secure download
    path('download-file/file/<uuid:file_id>/', FileDownloadView.as_view(), name='file-download'),
    path('download-file/token/<uuid:token>/', SecureFileDownloadView.as_view(), name='secure-file-download'),
    path('generate-token/<uuid:file_id>/', FileDownloadTokenView.as_view(), name='generate-token'),
]

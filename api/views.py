from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomUser, File, DownloadToken
from .serializers import FileSerializer, UserSerializer
from .permissions import IsVerifiedClientUser
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
import uuid
from datetime import timedelta

# Auth Views
class OpsLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class ClientLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

# File Views
class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        file = self.request.FILES['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ['pptx', 'docx', 'xlsx']:
            raise serializer.ValidationError("Invalid file type")
        serializer.save(uploaded_by=self.request.user)

class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return File.objects.all()

class FileDownloadView(generics.RetrieveAPIView):
    def get(self, request, token):
        try:
            download_token = DownloadToken.objects.get(
                token=token,
                expires_at__gt=timezone.now(),
                used=False
            )
            if request.user != download_token.user or request.user.role != 'CLIENT':
                return Response({"error": "Access denied"}, status=403)
            
            download_token.used = True
            download_token.save()
            return Response({
                "download-link": request.build_absolute_uri(download_token.file.file.url),
                "message": "success"
            })
        except DownloadToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=404)

# User Views
class ClientSignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(role='CLIENT')
        verification_token = uuid.uuid4()
        verification_url = self.request.build_absolute_uri(
            reverse('verify-email') + f'?token={verification_token}'
        )
        send_mail(
            'Verify Email',
            f'Click here to verify: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({"url": verification_url}, status=201)

class EmailVerifyView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        # Implement token verification logic
        return Response({"message": "Email verified"})


# api/views.py
from django.shortcuts import render

def frontend(request):
    return render(request, 'frontend.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import File

class FileDownloadView(APIView):
    def get(self, request, file_id):
        try:
            file = File.objects.get(id=file_id)
            # ... generate download token/link logic ...
            return Response({
                "download_link": f"http://localhost:8000/api/download-file/{file_id}/securetoken...",
                "message": "success"
            })
        except File.DoesNotExist:
            return Response({"detail": "File not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from django.http import FileResponse
from .models import File, DownloadToken
from django.utils import timezone

class SecureFileDownloadView(APIView):
    authentication_classes = []  # No JWT required for this endpoint
    permission_classes = []      # Security is via the token

    def get(self, request, file_id, token):
        try:
            download_token = DownloadToken.objects.get(
                token=token,
                file_id=file_id,
                expires_at__gt=timezone.now(),
                used=False
            )
            # Optionally: check download_token.user matches intended user

            # Mark token as used
            download_token.used = True
            download_token.save()

            file_obj = download_token.file.file
            return FileResponse(file_obj.open('rb'), as_attachment=True, filename=file_obj.name)
        except DownloadToken.DoesNotExist:
            return Response({"detail": "Invalid or expired token"}, status=404)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import File, DownloadToken

class FileDownloadTokenView(APIView):
    permission_classes = [IsVerifiedClientUser]  # Only verified clients

    def get(self, request, file_id):
        try:
            file = File.objects.get(id=file_id)
            token = DownloadToken.objects.create(
                file=file,
                user=request.user,
                expires_at=timezone.now() + timedelta(minutes=5)
            )
            download_url = request.build_absolute_uri(
                f"/api/download-file/{file_id}/{token.token}/"
            )
            return Response({
                "download_url": download_url,
                "message": "success"
            })
        except File.DoesNotExist:
            return Response({"detail": "File not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from .models import File, DownloadToken, CustomUser
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from .models import File, DownloadToken
from .permissions import IsVerifiedClientUser  # Ensure this is defined

class FileDownloadTokenView(APIView):
    """
    Generates a secure download token and URL for client users.
    Requires authenticated and verified client user.
    """
    permission_classes = [IsVerifiedClientUser]

    def get(self, request, file_id):
        try:
            # 1. Get the requested file
            file = File.objects.get(id=file_id)
            
            # 2. Create a download token (valid for 5 minutes)
            token = DownloadToken.objects.create(
                file=file,
                user=request.user,
                expires_at=timezone.now() + timedelta(minutes=5)
            )
            
            # 3. Generate secure download URL
            download_url = request.build_absolute_uri(
                reverse('secure-file-download', args=[str(token.token)])
            )
            
            # 4. Return the URL to client
            return Response({
                "download_url": download_url,
                "message": "success",
                "expires_at": token.expires_at.isoformat()
            })
            
        except File.DoesNotExist:
            return Response(
                {"detail": "File not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SecureFileDownloadView(APIView):
    authentication_classes = []  # No JWT needed
    permission_classes = []  # Security via token

    def get(self, request, token):
        try:
            download_token = DownloadToken.objects.get(
                token=token,
                expires_at__gt=timezone.now(),
                used=False
            )
            # Validate client user
            if download_token.user.role != 'CLIENT':
                return Response({"detail": "Access denied"}, status=status.HTTP_403_FORBIDDEN)
                
            # Mark token as used
            download_token.used = True
            download_token.save()
            
            # Serve the file
            file_obj = download_token.file.file
            return FileResponse(file_obj.open('rb'), 
                               as_attachment=True, 
                               filename=file_obj.name)
            
        except DownloadToken.DoesNotExist:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_404_NOT_FOUND)

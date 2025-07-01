# from django.urls import reverse
# from rest_framework.test import APITestCase
# from .models import CustomUser

# class FileSharingTests(APITestCase):
#     def setUp(self):
#         self.ops_user = CustomUser.objects.create_user(
#             username='ops', password='password', role='OPS'
#         )
#         self.client_user = CustomUser.objects.create_user(
#             username='client', password='password', role='CLIENT', email_verified=True
#         )
    
#     def test_ops_upload(self):
#         self.client.force_authenticate(user=self.ops_user)
#         response = self.client.post(reverse('file-upload'), {'file': file})
#         self.assertEqual(response.status_code, 201)
    
#     # Add tests for all scenarios

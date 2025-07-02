from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, File

# Optional: Custom forms if you have extra fields
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'email_verified')}),
    )

# Register your custom user model
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'uploaded_by', 'uploaded_at']
    search_fields = ['uploaded_by__username']

# If you have other models, register them similarly
# from .models import DownloadToken
# admin.site.register(DownloadToken)
# Developed by SACHIN VARDHAN

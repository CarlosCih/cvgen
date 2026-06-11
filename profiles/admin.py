from django.contrib import admin
from .models import Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'degree', 'school', 'university')
    search_fields = ('name', 'email', 'phone', 'degree', 'school', 'university')
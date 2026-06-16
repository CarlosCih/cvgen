from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('create/', views.CVCreateView.as_view(), name='create_profile'),
    path('resume/<int:id>/', views.resume, name='resume'),
    path('download/<int:id>/', views.DownloadPDF, name='download_pdf'),
    path('edit/<int:pk>/', views.CVUpdateView.as_view(), name='edit_profile'),
    path('delete/<int:id>/', views.CVDelete, name='delete_profile'),
]

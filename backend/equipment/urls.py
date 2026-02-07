from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.login_view, name='login'),
    
    # CSV Upload
    path('upload/', views.CSVUploadView.as_view(), name='csv-upload'),
    
    # Datasets
    path('datasets/', views.DatasetListView.as_view(), name='dataset-list'),
    path('datasets/<int:pk>/', views.DatasetDetailView.as_view(), name='dataset-detail'),
    path('datasets/<int:pk>/summary/', views.DatasetSummaryView.as_view(), name='dataset-summary'),
    path('datasets/<int:pk>/report/', views.GeneratePDFReportView.as_view(), name='dataset-report'),
]

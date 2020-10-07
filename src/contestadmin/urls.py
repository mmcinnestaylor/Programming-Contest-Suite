from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('ec_files/', views.download_ec_files, name='all_ec_files'),
    path('ec_files/<uidb64>/', views.FacExtraCreditFiles.as_view(), name='fac_ec_files'),
]

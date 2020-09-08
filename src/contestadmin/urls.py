from django.urls import path

from . import views

urlpatterns = [
    # contest suite homepage
    path('ec_files/', views.download_ec_files, name='ec_files'),
]

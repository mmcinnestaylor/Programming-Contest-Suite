from django.urls import path

from . import views

urlpatterns = [
    # contest suite homepage
    path('', views.base, name='manage_base'),
    path('profile/', views.profile, name='manage_profile'),
]

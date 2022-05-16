from django.urls import path

from . import views

urlpatterns = [
    # contest suite homepage
    path('', views.dashboard, name='lfg_dashboard'),
]

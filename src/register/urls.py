from django.urls import path

from . import views

urlpatterns = [
    # contest suite registeration page
    path('', views.register, name='register'),
    path('account/', views.account, name='account'),
]

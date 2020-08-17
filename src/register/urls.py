from django.urls import path

from . import views

urlpatterns = [
    # contest suite registeration page
    path('', views.base, name='register_base'),
    path('account/', views.account, name='register_account'),
    path('team/', views.team, name='register_team'),
]

from django.urls import path

from . import views

urlpatterns = [
    # contest suite homepage
    path('', views.dashboard, name='lfg_dashboard'),
    path('profile/activate/', views.activate_profile, name='activate_lfg_profile'),
    path('profile/create/', views.create_profile, name='create_lfg_profile'),
    path('profile/deactivate/', views.deactivate_profile, name='deactivate_lfg_profile'),
    path('profile/manage/', views.manage_profile, name='manage_lfg_profile'),
]

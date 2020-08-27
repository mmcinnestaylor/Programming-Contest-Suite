from django.urls import path

from . import views

urlpatterns = [
    # contest suite homepage
    path('', views.base, name='manage_base'),
    path('profile/', views.profile, name='manage_profile'),
    path('courses/', views.courses, name='manage_courses'),
    path('courses/clear/', views.clear_courses, name='clear_courses'),
    path('team/', views.team, name='manage_team'),
    path('team/join/', views.join_team, name='join_team'),
    path('team/leave/', views.leave_team, name='leave_team'),
    path('team/delete/', views.delete_team, name='delete_team'),
    path('team/remove/<str:username>/', views.remove_member, name='remove_member'),
]

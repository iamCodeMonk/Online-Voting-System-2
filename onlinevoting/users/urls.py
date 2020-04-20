from django.urls import path
from . import views as users_views

urlpatterns = [
    path('' , users_views.profile ,name = 'profile'),
    path('society/',  users_views.society, name = 'My Societies'),
    path('society/<int:pk>/' , users_views.SocietyDetailView.as_view() ,name = 'society-detail'),
    path('society/new/', users_views.SocietyCreateView.as_view(), name = 'society_create')
]

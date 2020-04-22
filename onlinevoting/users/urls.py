from django.urls import path
from . import views as users_views

urlpatterns = [
    path('' , users_views.profile ,name = 'profile'),
    path('society/',  users_views.society, name = 'My Societies'),
    path('society/<id>/' , users_views.SocietyDetailView ,name = 'society-detail'),
    path('society/new/', users_views.SocietyCreateView.as_view(), name = 'society_create'),
    path('society/<id1>/<id2>' , users_views.SocietyApprovalView ,name = 'society_approve'),
]

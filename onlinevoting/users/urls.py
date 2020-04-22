from django.urls import path
from . import views as users_views
from queries import views as queries_views


urlpatterns = [
    path('' , users_views.profile ,name = 'profile'), #done
    path('society/',  users_views.society, name = 'My Societies'), #done
    path('society/new/', users_views.SocietyCreateView.as_view(), name = 'society_create'), #done
    path('society/<id>/' , users_views.SocietyDetailView ,name = 'society-detail'), #done
    path('society/<id1>/<id2>' , users_views.SocietyApprovalView ,name = 'society_approve'),
    path('society/<int:pk>/delete/' , users_views.SocietyDeleteView.as_view() ,name = 'society-delete'),
    path('society/<int:pk>/<str:Name>/queries/', queries_views.PostListView.as_view(), name = 'queries-home'),#done
    path('society/<int:pk>/<str:Name>/queries/new', queries_views.PostCreateView.as_view(), name = 'new-query'),#done
]

from django.urls import path
from .views import UserView, UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),  # Only GET (list), POST (create)
    path('<int:user_id>/', UserView.as_view(), name='user-detail'),  # GET, PUT, PATCH, DELETE for single user
] 
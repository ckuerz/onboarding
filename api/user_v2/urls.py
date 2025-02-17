from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_user, name='user-v2-create'),
    path('<int:user_id>/', views.user_detail, name='user-v2-detail'),
] 
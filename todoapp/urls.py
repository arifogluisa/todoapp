from django.urls import path
from .views import (TaskListView,TaskCreateView, TaskDetailView,
TaskUpdateView, TaskDeleteView, CustomLoginView,
RegisterUser, comment_remove, comment_update)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create-task/', TaskCreateView.as_view(), name='task_create'),
    path('update-task/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('delete-task/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('comment-update/<int:pk>/', comment_update, name='comment_update'),
    path('comment-delete/<int:pk>/', comment_remove, name='comment_delete'),
    

]
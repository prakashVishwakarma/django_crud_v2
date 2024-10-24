# api/urls.py

from django.urls import path
from .views import CreateTaskView, CreateTaskViewGetById, TaskDeleteView, UserProfileCurdView, UpdateUserProfile, AuthorCreateView

urlpatterns = [
    path('mymodel/', CreateTaskView.as_view(), name='mymodel'),
    path('getmymodel/', CreateTaskView.as_view(), name='getmymodel'),
    path('getbyid/<int:task_id>/', CreateTaskViewGetById.as_view(), name='getbyid'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('put/<int:pk>/', TaskDeleteView.as_view(), name='put'),
    # one_to_one
    path('create/', UserProfileCurdView.as_view(), name='create'),
    path('get_all/', UserProfileCurdView.as_view(), name='get_all'),
    path('get_by_id/<int:user_id>/', UserProfileCurdView.as_view(), name='get_by_id'),
    path('put_one_by_one/<int:user_id>/', UpdateUserProfile.as_view(), name='put'),
    # one_to_many
    path('post_one_to_many/', AuthorCreateView.as_view(), name='AuthorCreateView'),
]

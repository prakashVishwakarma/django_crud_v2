# api/urls.py

from django.urls import path
from .views import CreateTaskView, CreateTaskViewGetById

urlpatterns = [
    path('mymodel/', CreateTaskView.as_view(), name='mymodel'),
    path('getmymodel/', CreateTaskView.as_view(), name='getmymodel'),
    path('getbyid/<int:task_id>/', CreateTaskViewGetById.as_view(), name='getbyid'),
]

# api/urls.py

from django.urls import path
from .views import CreateTaskView

urlpatterns = [
    path('mymodel/', CreateTaskView.as_view(), name='mymodel'),
    path('getmymodel/', CreateTaskView.as_view(), name='getmymodel'),
]

from django.contrib import admin
from .models import Task, CrudUser, UserProfile

admin.site.register(Task)
admin.site.register(CrudUser)
admin.site.register(UserProfile)

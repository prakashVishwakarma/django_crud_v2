from django.contrib import admin
from .models import Task, CrudUser, UserProfile, Author, Book

admin.site.register(Task)
admin.site.register(CrudUser)
admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)

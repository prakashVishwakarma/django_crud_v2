from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# User and UserProfile models with a one-to-one relationship
class CrudUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()

class UserProfile(models.Model):
    user = models.OneToOneField(CrudUser, on_delete=models.CASCADE)
    bio = models.TextField()
    website = models.URLField(null=True, blank=True)

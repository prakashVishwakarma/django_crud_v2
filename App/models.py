from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# User and UserProfile models with a one-to-one relationship - start

class CrudUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()

class UserProfile(models.Model):
    user = models.OneToOneField(CrudUser, on_delete=models.CASCADE)
    bio = models.TextField()
    website = models.URLField(null=True, blank=True)

# User and UserProfile models with a one-to-one relationship - end

# Author and Post models with a one-to-many relationship - start

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name

# Author and Post models with a one-to-many relationship - end

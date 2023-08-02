from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    painter = models.CharField(max_length=30)
    drawing_technique = models.CharField(max_length=50)
    work_year = models.CharField(max_length=20)
    content = models.TextField()
    type_choices = [("고전미술", "고전미술"), ("현대미술", "현대미술")]
    type = models.CharField(max_length=128, choices=type_choices)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

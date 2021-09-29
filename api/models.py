from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    body = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    slug = models.CharField(max_length=200, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title




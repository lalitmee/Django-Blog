from django.db import models
from django.contrib.auth.models import Permission, User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    #user = models.ForeignKey(User, default=1)
    author = models.ForeignKey('auth.User', default=1)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

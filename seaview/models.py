from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    postname = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.postname

class Reply(models.Model):
    postname = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

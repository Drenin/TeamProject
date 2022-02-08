from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=30)  # 제목
    genre = models.CharField(max_length=15)
    year = models.IntegerField()

    def __str__(self):
        return self.title

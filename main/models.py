from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(unique=True, max_length=200)
    user_pw = models.CharField(max_length=200)
    user_name = models.CharField(max_length=30)
    validation = models.BooleanField(default=False)
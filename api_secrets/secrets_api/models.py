from django.db import models

# Create your models here.
class SECRET(models.Model):
    name = models.CharField(max_length=200, primary_key=True, default="")
    SECRET_KEY = models.CharField(max_length=200)
    DEBUG = models.CharField(max_length=200, default='True')

from django.db import models

# Create your models here.
class SECRET(models.Model):
    name = models.CharField(max_length=200, primary_key=True, default="")
    SECRET_KEY = models.CharField(max_length=200)
    DEBUG = models.CharField(max_length=200, default='True')
    DB_DEFAULT_ENGINE = models.CharField(max_length=200)
    DB_DEFAULT_NAME = models.CharField(max_length=200)

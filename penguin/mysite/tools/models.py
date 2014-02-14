from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	areaCode = models.CharField(max_length=30)

class Tool(models.Model):
	name = models.CharField(max_length=30)

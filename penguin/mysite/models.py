from django.db import models

# Create your models here.
class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	areaCode = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	phone_number = models.CharField(max_length=10)
	is_shed_coordinator = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	

class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	owner = models.ForeignKey('User')
	is_borrowed = models.BooleanField(default=False)
	description = models.CharField(max_length=250)
	
class BorrowTransaction(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('User')
	borrower = models.ForeignKey('User')
	tool = models.ForeignKey('Tool')
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
  
class User(AbstractUser):
	is_kurir = models.BooleanField('user kurir',default=False)
	is_manager = models.BooleanField('user manager',default=False)
	is_admin = models.BooleanField('user admin',default=False)

class Rice(models.Model):
	name = models.CharField(max_length=255)
	stock = models.IntegerField()
	price = models.IntegerField()
#Quize
class Distribution(models.Model):
	name = models.CharField(max_length=255)
	ordered_by = models.CharField(max_length=255)
	address = models.TextField()
	telepon = models.CharField(max_length=14, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	catatan_khusus = models.TextField(blank=True, null=True)
	statusOrder = models.CharField(max_length=1, blank=True, null=True)

class DetailOrder(models.Model):
	distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='detail_orders')
	rice = models.ForeignKey(Rice, on_delete=models.CASCADE, related_name='detail_orders')
	value = models.IntegerField()
	prices = models.CharField(max_length=255, blank=True, null=True)

#student
class Kurir(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	distributions = models.ManyToManyField(Distribution, through='TakenDistribution')
	email = models.EmailField(max_length=500)
	no_hp = models.CharField(max_length=13)
	alamat = models.TextField()
	status_akun = models.CharField(max_length=1,blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)

#TakenQuiz
class TakenDistribution(models.Model):
	kurir = models.ForeignKey(Kurir, on_delete=models.CASCADE, related_name='taken_distributions')
	distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='taken_distributions')
	date = models.DateTimeField(auto_now_add=True)
	status_antar = models.CharField(max_length=300, blank=True, null=True)
	status_track = models.CharField(max_length=1, blank=True, null=True)
	status = models.CharField(max_length=1, blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)

class DataLogPerjalanan(models.Model):
	taken_distribution = models.ForeignKey(TakenDistribution, on_delete=models.CASCADE, related_name='datalog_perjalanan')
	date = models.DateTimeField(auto_now_add=True)
	x = models.TextField(blank=True, null=True)
	y = models.TextField(blank=True, null=True)
	z = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=300, blank=True, null=True)
	location = models.TextField(blank=True, null=True)

class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	email = models.EmailField(max_length=500)
	no_hp = models.CharField(max_length=13)
	alamat = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)

class PortalSignUp(models.Model):
	port_kurir = models.CharField(max_length=1)
	port_manager = models.CharField(max_length=1)
	port_admin = models.CharField(max_length=1)
	token_kurir = models.TextField(blank=True, null=True)
	token_manager = models.TextField(blank=True, null=True) 
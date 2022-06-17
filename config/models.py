from django.db import models
import uuid

class Config(models.Model):
	device_name = models.CharField(max_length=155, blank=False)
	ipaddress = models.GenericIPAddressField(unique=True, blank=False)
	key = models.CharField(max_length=155,unique=True, default=uuid.uuid4(), blank=False)

	def __str__(self):
		return self.device_name


class TokenApi(models.Model):
	device = models.ForeignKey(Config, on_delete=models.CASCADE)
	token = models.CharField(max_length=255, blank=False)
	valid_until = models.DateTimeField(blank=False)

	def __str__(self):
		return self.device.device_name


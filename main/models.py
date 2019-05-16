from __future__ import unicode_literals
from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.

class Campaign(models.Model):
	
	name = models.CharField(max_length=255, blank=True)

class Temp(models.Model):

	name = models.CharField(max_length=100, null=True, default=None, blank=True)
	URL = models.FileField(upload_to='documents/', default=None)   
	campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default=None, null=True, blank=True)

@receiver(post_delete, sender=Temp)
def submission_delete(sender, instance, **kwargs):
    instance.URL.delete(False) 

class ClientsInfo(models.Model):

    name = models.CharField(max_length=255, blank=True)
    lastName = models.CharField(max_length=255, blank=True)
    phoneNumber = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default=None, null=True, blank=True)
   
class TableColumns(models.Model):

	name = models.CharField(max_length=255, blank=True)
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Strategy(models.Model):
    description = models.CharField(max_length=500,null=True,blank=True)
    name = models.CharField(max_length=80,default=' استراتژی من ')
    filters = models.CharField(max_length=500)
    config = models.CharField(max_length=500,null=True,blank=True)
    watch_list = models.CharField(max_length=500)


class Follower(models.Model):
    owner = models.ForeignKey(User)
    strategy = models.ForeignKey(Strategy)
    follower = models.ForeignKey(User)

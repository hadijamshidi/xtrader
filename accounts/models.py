from django.db import models

# Create your models here.

from django.db.models import (Model,
                              OneToOneField,
                              DateField, )
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class Subscribe(models.Model):
    name = models.CharField(max_length=11, verbose_name='نام پکیج')
    price = models.IntegerField()
    value = models.IntegerField()


class Profile(UserenaBaseProfile):
    user = OneToOneField(User,
                         unique=True,
                         verbose_name=_('user'),
                         related_name='my_profile')
    cellPhone = models.CharField(max_length=11, verbose_name='شماره تلفن ', null=True, blank=True)
    expire = models.DateField(null=True, blank=True)

    def last_login(self):
        return self.user.last_login

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Membership(models.Model):
    subscribe = models.ForeignKey(Subscribe)
    profile = models.ForeignKey(Profile)

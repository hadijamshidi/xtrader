from django.db import models
from django.utils import timezone
# Create your models here.
import datetime
from datetime import datetime as dt
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
    vip = models.BooleanField(default=0, verbose_name='ویژه')

    def __str__(self):
        return self.name + str(self.value)


class Profile(UserenaBaseProfile):
    user = OneToOneField(User,
                         unique=True,
                         verbose_name=_('user'),
                         related_name='my_profile')
    cellPhone = models.CharField(max_length=11, verbose_name='شماره تلفن ', null=True, blank=True)

    expire = models.DateField(default=timezone.now() + datetime.timedelta(10))

    def last_login(self):
        return self.user.last_login

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def have_subscribe(self):
        from sales.models import Payment
        payment = Payment.objects.filter(membership__profile=self).filter(success=True).last()
        if payment:
            if self.expire >= dt.today().date():
                return payment.membership.subscribe.name
            else:
                return 0
        else:
            return 0


class Membership(models.Model):
    subscribe = models.ForeignKey(Subscribe)
    profile = models.ForeignKey(Profile)

    def success(self):
        from sales.models import Payment
        return Payment.objects.all().filter(membership=self).first().success

    # def __str__(self):
    #     return self.subscribe.name

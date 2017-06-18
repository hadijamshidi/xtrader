from django.db import models

# Create your models here.

from django.db.models import (Model,
                              OneToOneField,
                              DateField,)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
class Profile(UserenaBaseProfile):
    user = OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    date_of_birth = DateField(blank=True, null=True)

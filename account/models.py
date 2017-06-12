from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (Model,
                              OneToOneField,
                              DateField,
                              ImageField)


class Profile(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, related_name='account_profile')
    date_of_birth = DateField(blank=True, null=True)
    photo = ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

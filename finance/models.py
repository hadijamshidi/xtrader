from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Strategy(models.Model):
    description = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=80, default=' استراتژی من ')
    filters = models.TextField()
    config = models.CharField(max_length=500, null=True, blank=True)
    watch_list = models.TextField()

    def loads(self):
        print(self.config)
        strategy_dict = dict(
            filters=[],
            watch_list=eval(self.watch_list),
            # TODO: include backtest config
            # config=eval(self.config),
        )
        for filter in eval(self.filters):
            strategy_dict['filters'].append(eval(filter))
        return strategy_dict

class Follower(models.Model):
    owner = models.ForeignKey(User, related_name='Owner')
    strategy = models.ForeignKey(Strategy, related_name='Strategy')
    follower = models.ForeignKey(User, related_name='Follower')

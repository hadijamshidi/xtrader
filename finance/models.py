from django.db import models

# Create your models here.
class strategy(models.Model):
	description = models.Charfield(max_length=500)
	name = models.Charfield(max_length=80)
	filters = models.Charfield(max_length=500)
	config = models.Charfield(max_length=500)
	watch_list = models.Charfield(max_length=500)
	
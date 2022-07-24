from django.db import models

class Venue(model.Model):
	name = models.CharField('Venue Name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code', max_length=15)
	phone =
	web =
	email =

class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	event_date = models.DateTimeField('Event Date')
	venue = models.CharField(max_length=120)
	manager = models.CharField(max_length=60)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

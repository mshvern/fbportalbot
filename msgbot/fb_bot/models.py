from django.db import models


# Create your models here.
class Movie(models.Model):
	movie_id = models.AutoField(primary_key=True)
	film_id = models.CharField(max_length=50, unique=True)
	title = models.CharField(max_length=225)
	all_shows_today = models.CharField(max_length=225, blank=True, null=True)
	show_start = models.CharField(max_length=225)
	show_end = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	director = models.CharField(max_length=255)
	format = models.CharField(max_length=255, blank=True, null=True)
	genres = models.CharField(max_length=255)
	year = models.CharField(max_length=255)
	duration = models.CharField(max_length=255)
	actors = models.CharField(max_length=255)
	trailer = models.CharField(max_length=255)
	poster = models.CharField(max_length=255)
	# Only if we decide that we need to show the schedule for the whole week
	# Which doesn't seem to be necessary, considering the schedule for the day is 100% identical to each day in the week
	# schedule = models.CharField(max_length=255, blank=True, null=True)
	already_out = models.IntegerField()

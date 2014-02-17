from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


# need to adjust Entry time function for start and end on the same date
 
class Employee(models.Model):
	user = models.OneToOneField(User)
	department = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=17)
	hire_date = models.DateTimeField()

	def __unicode__(self):
		name = self.user.first_name
		return name

	def total_time_debit(self):
		total_time = 0
		for entry in self.entry_set.all():
			total_time += entry.total_hours()
		return total_time

class Entry(models.Model):
	VACATION = 1
	SICK_DAY = 2
	PERSONAL_DAY = 3
	
	Status_Choices = {
		(VACATION, 'Vacation'),
		(SICK_DAY, 'Sick Day'),
		(PERSONAL_DAY, 'Personal Day'),
	}

	user = models.ForeignKey(Employee)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True,)
	status = models.IntegerField(choices=Status_Choices, default=VACATION)
	comment = models.TextField()
	request_date = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.comment

	def total_hours(self):

		# round start and end times to calculate calander days, not chunks of 24 hours
		rounded_start = self.start_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		rounded_end = self.end_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		end_date_start = self.end_date.replace(hour = 12, minute = 30, second = 0, microsecond = 0)
		
		days = (rounded_end - rounded_start).days

		end_day = self.end_date - end_date_start
		seconds = end_day.total_seconds()
		hours = seconds // 3600.0
		minutes = (seconds % 3600) // 60
		# check to see if we need to deduct 30 minutes for lunch
		if (self.end_date.hour >= 17):
			minutes -= 30

		hours += (minutes / 60)
		hours += days*8

		return hours

class Approval(models.Model):
	entry_id = models.ForeignKey(Entry)
	approved_by = models.ForeignKey(Employee)
	approved_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s for %s' % (self.approved_by, self.entry_id)

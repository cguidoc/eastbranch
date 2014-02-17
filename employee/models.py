from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from dateutil import rrule


# need to adjust Entry time function for start and end on the same date
# need to adjust Entry time function to exclude weekends
# need to adjust Entry time function to calculate not full days
# calculate start subtraction (start time - 7:30)
# calculate end subtraction	(4 - end time)
# subtract both from days*8 (total hours)
 
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
		# create new datetime objects for the start and end of the entry
		# use these to calculate the incomplete days at the start and end of the entry
		# we count the total number of days using the rrule, then subtract the incomplete days at the start and end

		end_date_end = self.end_date.replace(hour = 21, minute = 00, second = 0, microsecond = 0)
		start_date_start = self.start_date.replace(hour = 12, minute = 30, second = 0, microsecond = 0)

		# calculate the number of minutes at the start of the entry
		start_offset = self.start_date - start_date_start
		start_offset_minutes = (start_offset.total_seconds() /60 )

		# calculate the number of minutes at the end of the entry
		end_offset = end_date_end - self.end_date
		end_offset_minutes = (end_offset.total_seconds() / 60 ) 

		# calculate the total number of days the entry spans - an incomplete day still counts as 1 day
		days = rrule.rrule(rrule.DAILY, byweekday=range(0,5), dtstart=self.start_date, until=self.end_date)
		days = len(list(days))
		
		# calculate the total number of minutes to offset the entry
		minutes = start_offset_minutes + end_offset_minutes		# offset for incomplete days
		minutes += days * 30									# auto deduct for lunch times
		
		# add back the lunch deduction if end time is before lunch
		if (self.end_date.hour in range(12, 17)):
			minutes -= 30
		
		hours = days * 8.5

		# now deduct the offsets
		hours -= (minutes / 60)

		return hours

class Approval(models.Model):
	entry_id = models.ForeignKey(Entry)
	approved_by = models.ForeignKey(Employee)
	approved_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s for %s' % (self.approved_by, self.entry_id)

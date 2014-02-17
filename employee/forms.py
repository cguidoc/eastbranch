from django.forms import ModelForm
from django import forms
from employee.models import Employee, Entry
from bootstrap3_datetime.widgets import DateTimePicker

# https://pypi.python.org/pypi/django-bootstrap3-datetimepicker

# need to validate start and end times are with in working hours

class RequestForm(ModelForm):
	start_date = forms.DateTimeField(
			widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm',}))
	end_date = forms.DateTimeField(
			widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm',}))
	class Meta:
		model = Entry
		exclude =['user']

	def clean(self):
		cleaned_data = super(RequestForm, self).clean()
		start = cleaned_data.get("start_date")
		end = cleaned_data.get("end_date")

		end_date_start = self.end_date.replace(hour = 12, minute = 30, second = 0, microsecond = 0)
		
		
		if (end < start):
			msg = u"End date must after start date"
			self._errors['start_date'] = self.error_class([msg])
			self._errors['end_date'] = self.error_class([msg])

			del cleaned_data['start_date']
			del cleaned_data['end_date']

		if (end)
		return cleaned_data
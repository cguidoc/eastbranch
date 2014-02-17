from django.forms import ModelForm
from django import forms
from employee.models import Employee, Entry
from bootstrap3_datetime.widgets import DateTimePicker

# https://pypi.python.org/pypi/django-bootstrap3-datetimepicker


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
		start_error=False
		end_error=False

		if (end == start):
			msg = u"Start and End can not be the same"
			self._errors['start_date'] = self.error_class([msg])
			self._errors['end_date'] = self.error_class([msg])
			start_error=True
			end_error=True
		
		if (end < start):
			msg = u"End Date must be before the start date" 
			self._errors['start_date'] = self.error_class([msg])
			self._errors['end_date'] = self.error_class([msg])
			start_error=True
			end_error=True

		if (end.hour not in range(7,16)):
			msg = u"End time not during working hours"
			self._errors['end_date'] = self.error_class([msg])
			end_error=True

		if (start.hour not in range(7,16) and start.minute < 30 ):
			msg = u"Start time not during working hours"
			self._errors['end_date'] = self.error_class([msg])
			start_error=True
		if start_error:
			del cleaned_data['start_date']
		if end_error:
			del cleaned_data['end_date']
		return cleaned_data
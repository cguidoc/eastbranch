from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from employee.models import Employee, Entry
from forms import RequestForm
from django import forms

def index(request):
	latest_employee_list = Employee.objects.all()
	context = {'latest_employee_list': latest_employee_list}
	return render(request, 'employees/index.html', context)

def detail(request, employee_id):
	employee = get_object_or_404(Employee, pk=employee_id)
	total_time = employee.total_time_debit()
	return render(request, 'employees/detail.html', {'employee': employee, 'debit': total_time })

def add(request, employee_id):
	employee = get_object_or_404(Employee, pk=employee_id)
	if request.method == 'POST':
		form = RequestForm(request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.user = Employee.objects.get(pk=employee_id)
			new_entry.save()
			return HttpResponseRedirect(reverse('employees:detail', args=(employee_id,)))
	else:
		print "not valid - returning"
		form = RequestForm()
	return render(request, 'employees/add.html', {'form': form, 'employee': employee})

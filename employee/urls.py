from django.conf.urls import patterns, url

from employee import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<employee_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<employee_id>\d+)/add/$', views.add, name='add'),
	url(r'^(?P<entry_id>\d+)/approve/$', views.approve, name='approve'),
)
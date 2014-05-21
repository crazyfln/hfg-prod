from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from .views import *


urlpatterns = patterns('app.views',
    # Examples:
    url(r'^error/', 'error', name='error'),
    url(r'^404/', '_404', name='404'),
    url(r'^$', 'index', name='index'),
    url(r'^facility/(?P<slug>[-\w]+)/$', Facility.as_view(), name='facility_details'),
    url(r'^favorites/$', 'favorites', name='favorites'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^create_customer/', 'create_customer', name='create_customer'),
    (r'^$', TemplateView.as_view(template_name="index.html")),
)

from .signals import * #ensure that the signals are attatched via import

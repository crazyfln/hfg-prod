from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from .views import *


urlpatterns = patterns('app.views',
    # Examples:
    url(r'^error/', 'error', name='error'),
    url(r'^404/', '_404', name='404'),
    url(r'^$', 'index', name='index'),
    url(r'^facility/(?P<slug>[-\w]+)/favorite/$', 'facility_favorite', name='favorite'),
    url(r'^facility/(?P<slug>[-\w]+)/request_phone/$', 'request_phone', name='request_phone'),
    url(r'^facility/(?P<slug>[-\w]+)/tour_request/$', 'tour_request', name='tour_request'),
    url(r'^facility/(?P<slug>[-\w]+)/open_tour_request/$', FacilityDetail.as_view(open_tour_request=True), name='open_tour_request'),
    url(r'^facility/(?P<slug>[-\w]+)/', FacilityDetail.as_view(), name='facility_details'),
    url(r'^search/', Search.as_view(), name='search'),
    url(r'^contact/$', Contact.as_view(), name='contact'),
    url(r'^profile/$', Profile.as_view(), name='profile'),
    url(r'^create_customer/', 'create_customer', name='create_customer'),
    url(r'^receive_reward/', 'receive_reward', name='receive_reward'),
    url(r'^making_move/', 'making_move', name='making_move'),
    url(r'^about/', 'about', name='about'),
    url(r'^home_video/', 'home_video', name='home_video'),
    url(r'^list_property/$', ListProperty.as_view(), name='list_property'),
    (r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^provider/change_facility_visibility/(?P<pk>[-\w]+)/$', 'change_facility_visibility', name='change_facility_visibility'),
    url(r'^manager/facility_note/(?P<pk>[-\w]+)/$', EditManagerNoteFacility.as_view(), name='edit_manager_note_facility'),
    url(r'^manager/invoice_note/(?P<pk>[-\w]+)/$', EditManagerNoteInvoice.as_view(), name='edit_manager_note_invoice'),

)

from .signals import * #ensure that the signals are attatched via import

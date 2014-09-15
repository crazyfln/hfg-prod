from django.shortcuts import render

from registration.backends.simple.views import RegistrationView as SimpleRegistrationView
from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import RegistrationForm
from app.models import Facility, PhoneRequest


## Make sure the view's base class matches the backend we're importing from
#class RegistrationView(DefaultRegistrationView):
class RegistrationView(SimpleRegistrationView):
    """ The class view that handles user registration. See
    https://bitbucket.org/ubernostrum/django-registration/src/8f242e35ef7c004e035e54b4bb093c32bf77c29f/registration/backends/simple/views.py?at=default#cl-11
    for an example of a simple way to use it
    """
    form_class = RegistrationForm
    request_tour = False
    ##Stick extra registration logic here
    def register(self, request, **cleaned_data):
        new_user = super(RegistrationView, self).register(request, **cleaned_data)
        new_user.first_name = cleaned_data['first_name']
        new_user.phone = cleaned_data['phone_number']
        new_user.last_name = cleaned_data['last_name']
        new_user.save()
        if self.kwargs.get('phone_or_tour') == 'phone' and self.kwargs.get('facility_slug'):
            facility = get_object_or_404(Facility, slug=self.kwargs['facility_slug'])
            phone_request = PhoneRequest(facility=facility, user=new_user)
            phone_request.save()
        return new_user

    def get_success_url(self, request, user):
        """
        Return the url a user should be redirected to after registration
        """
        if self.kwargs.get('phone_or_tour') == 'tour' and self.kwargs.get('facility_slug'):
            query_string = request.META['QUERY_STRING']
            full_url = query_string.split('next=')[1]
            url_parts = full_url.split('?')
            url = url_parts[0] + 'open_tour_request/'
            if len(url_parts) > 1: 
                url += '?' + url_parts[1]
        else:
            url = str(request.GET.get('next', reverse('index')))
            
        return url

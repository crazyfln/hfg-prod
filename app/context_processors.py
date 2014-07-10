from django.conf import settings as django_settings

from .forms import ListPropertyForm 

def settings(request):
    settings = {
        'SETTINGS': django_settings,
    }

    return settings

def property_list_form(request):
    return {'property_list_form': ListPropertyForm() }

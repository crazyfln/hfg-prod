from django.conf import settings as django_settings

from .forms import ListPropertyForm 

def settings(request):
    settings = {
        'SETTINGS': django_settings,
    }

    return settings

def property_list_form(request):
    return {'property_list_form': ListPropertyForm() }

def google_analytics(request):
    """
    Returns variables to render your Google Analytics tracking code template.
    """
    ga_prop_id = getattr(django_settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ga_domain = getattr(django_settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not django_settings.DEBUG and ga_prop_id and ga_domain:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}

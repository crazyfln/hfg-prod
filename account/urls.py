from django.conf.urls import patterns, include, url

from .views import RegistrationView
from .forms import AuthenticationForm


urlpatterns = patterns('',
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    (r'^login/$', 'django.contrib.auth.views.login', {'authentication_form': AuthenticationForm, 'template_name': 'registration/login.html',}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),


)



###Simple backend doesn't do email confirmation
urlpatterns += patterns('app.views',
    (r'', include('registration.backends.simple.urls')),
)

###default backend does  email confirmation

# urlpatterns = patterns('app.views',
#     (r'', include('registration.backends.default.urls')),
# )

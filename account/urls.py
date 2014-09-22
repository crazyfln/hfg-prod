from django.conf.urls import patterns, include, url
from django.contrib.auth import views

from .views import RegistrationView
from .forms import AuthenticationForm


urlpatterns = patterns('',
    url(r'^register/(?P<facility_slug>[-\w]+)/(?P<phone_or_tour>[-\w]+)/$', RegistrationView.as_view(), name='registration_and'),
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    (r'^login/$', 'django.contrib.auth.views.login', {'authentication_form': AuthenticationForm, 'template_name': 'registration/login.html',}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^password_change/$', views.password_change, name="password_change", kwargs={'post_change_redirect':'/profile'}),


)



###Simple backend doesn't do email confirmation
urlpatterns += patterns('app.views',
    (r'', include('registration.backends.simple.urls')),
)

###default backend does  email confirmation

# urlpatterns = patterns('app.views',
#     (r'', include('registration.backends.default.urls')),
# )

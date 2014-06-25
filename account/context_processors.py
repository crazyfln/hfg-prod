from django.core.urlresolvers import reverse

from .forms import RegistrationForm, AuthenticationForm

def forms(request):
    forms = {}
    if request.user.is_authenticated():
        return forms
    if not request.get_full_path() == reverse("django.contrib.auth.views.login"):
        forms['login_form'] = AuthenticationForm()
    if not request.get_full_path() == reverse("registration_register"):
        forms['registration_form'] = RegistrationForm()
#    if not request.get_full_path() == reverse("password_reset"):
#        forms['fpassword_form'] = PasswordResetForm()
    return forms

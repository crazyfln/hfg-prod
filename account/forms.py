import re

from django import forms 
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from app.models import Condition
from app.facility_message_mixin import field_choices, field_choices_empty, FacilityMessageFormFieldMixin

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    # email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))



class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    """
    username = forms.CharField(widget=forms.HiddenInput,required=False)

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    email = forms.EmailField(label=_("E-mail"), required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                                label=_("Password"))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirm'}),
                                label=_("Password"))
    



    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

        username = (self.cleaned_data.get('email', "bad@email.com").split("@")[0]).lower()
        username = re.sub('\W', "", username)

        otherusers = User.objects.filter(username__startswith=username).count()
        username = username + str(otherusers)
        self.cleaned_data['username'] = username
        return self.cleaned_data


    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        numbers = re.findall('\d', data)
        number = ''.join(str(s) for s in numbers)
        if not len(number) == 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")
        return number

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return ""

class ProfileForm(FacilityMessageFormFieldMixin, ModelForm):
    conditions = forms.ModelMultipleChoiceField(
        queryset=Condition.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'id':'id_condition'})
    )
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone', \
            'budget', 'conditions', 'searching_for','health_description','resident_first_name','preferred_contact', 'planned_move_date', \
            'pay_private_pay','pay_longterm_care','pay_veterans_benefits','pay_medicare','pay_medicaid','pay_ssi', \
            'care_bathing','care_diabetic','care_medical_assistance','care_medical_assistance','care_toileting','care_memory_issues','care_diagnosed_memory','care_combinative','care_wandering')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['conditions'].initial = self.instance.conditions.all()

        for field in self.fields:
            if self.fields[field].widget.__class__.__name__ == 'CheckboxInput':
                  self.fields[field].label = ""

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)

        if commit:
            user.save()

        if user.pk:
            user.conditions = self.cleaned_data.get('conditions')
            self.save_m2m()

        return user



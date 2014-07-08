import datetime
import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.forms import ModelForm, widgets
from django.forms.models import BaseInlineFormSet
from django.forms.extras.widgets import SelectDateWidget

from django.utils.translation import ugettext_lazy as _

from .models import *
from .facility_message_mixin import SEARCHING_FOR_CHOICES, BUDGET_CHOICES, MOBILITY_CHOICES, CARE_CURRENT_CHOICES, MOVE_IN_TIME_FRAME_CHOICES
SEARCH_MIN_VAL_INITIAL = "500"
SEARCH_MAX_VAL_INITIAL = "6000"

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='search', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search by City, Zip, Facility Name'}))
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), empty_label="All", required=False)
    facility_type = forms.ModelChoiceField(queryset=FacilityType.objects.all(), empty_label="All", required=False)
    amenities = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Amenity.objects.all(), required=False)
    min_value = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=SEARCH_MIN_VAL_INITIAL)
    max_value = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=SEARCH_MAX_VAL_INITIAL)

class ListPropertyForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description'}))

    def send_email(self):
        message = self.cleaned_data['descprtion'] + "<br/>"
        who = self.cleaned_data['first_name']
        send_mail(
                subject="Home For Grandma: Listing Request from" + who,
                message = message + "from: " + who,
                from_email=self.cleaned_data['email'],
                )

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Website'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))

    def send_email(self):
        message = self.cleaned_data['message'] + "<br />"
        who = self.cleaned_data['name']
        site = self.cleaned_data['website']
        send_mail(
                subject="Home For Grandma: contact us message from " + who,
                message= message + "from: " + who + "of - " + site, 
                from_email=self.cleaned_data['email'],
                recipient_list = [settings.CONTACT_EMAIL]
                )
            
BUDGET_CHOICES_EMPTY = [('','Budget')] + BUDGET_CHOICES
MOBILITY_CHOICES_EMPTY = [('','Mobility')] + MOBILITY_CHOICES
CARE_CURRENT_CHOICES_EMPTY = [('','Current Living Situation')] + CARE_CURRENT_CHOICES
MOVE_IN_TIME_FRAME_CHOICES_EMPTY = [('','Planned move-in Time Frame')] + MOVE_IN_TIME_FRAME_CHOICES
SEARCHING_FOR_CHOICES_EMPTY = [('','I%cm Searching for?' %39)] + SEARCHING_FOR_CHOICES

class TourRequestForm(ModelForm):
    budget = forms.ChoiceField(choices=BUDGET_CHOICES_EMPTY, required=False) 
    care_mobility = forms.ChoiceField(choices=MOBILITY_CHOICES_EMPTY, required=False)
    care_current = forms.ChoiceField(choices=CARE_CURRENT_CHOICES_EMPTY, required=False)
    move_in_time_frame = forms.ChoiceField(choices=MOVE_IN_TIME_FRAME_CHOICES_EMPTY, required=False)
    searching_for = forms.ChoiceField(choices=SEARCHING_FOR_CHOICES_EMPTY, required=False)

    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':"Tell us about your loved one. Health condition, concerns, hobbies, etc."}))
    health_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':"Describe your health condition"}))
    desired_city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':"Desired City"}))
    resident_first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':"Resident's First Name"}))

    class Meta:
        model = FacilityMessage
        exclude = ('user','facility','read','replied_by','replied_datetime')
        widgets = {'planned_move_date': forms.TextInput(attrs={'placeholder': 'Date', 'class':''})}
    
    def save(self, commit=True):
        new_request = super(TourRequestForm, self).save(commit=False)
        if commit:
            new_request.save()
        return new_request

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super(TourRequestForm, self).__init__(*args, **kwargs)
        if self.user:
            for field in self.fields:
                if hasattr(self.user, field):
                    self.fields[field].initial = getattr(self.user, field)
        for field in self.fields:
            if self.fields[field].widget.__class__.__name__ == 'CheckboxInput':
                self.fields[field].label = ""
            

class FacilityAdminForm(ModelForm):

    def clean_phone(self):
        data = self.cleaned_data['phone']
        numbers = re.findall('\d', data)
        number = ''.join(str(s) for s in numbers)
        if not len(number) == 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")
        return number

    class Meta:
        model = Facility
        widgets = {
            'description_long':forms.Textarea,
        }

class EditManagerNoteFacilityForm(ModelForm):

    class Meta:
        model = Facility
        fields = ('manager_note',)
        widgets = {
            'manager_note':forms.Textarea,
        }

class EditManagerNoteInvoiceForm(ModelForm):

    class Meta:
        model = Invoice
        fields = ('manager_note',)
        widgets = {
            'manager_note':forms.Textarea,
        }

class FacilityProviderForm(FacilityAdminForm):

    class Meta(FacilityAdminForm.Meta):
        exclude = ('holding_group',)

class StripeTokenForm(forms.Form):
    id = forms.CharField()


class ChargeForm(forms.Form):
    amount = forms.DecimalField(max_digits=5, decimal_places=2)

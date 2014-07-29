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
from ajax_select import make_ajax_field

from .models import *
from .facility_message_mixin import field_choices, field_choices_empty, FacilityMessageFormFieldMixin
from account.forms import CustomModelMultipleChoiceField
SEARCH_MIN_VAL_INITIAL = "500"
SEARCH_MAX_VAL_INITIAL = "6000"

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='search', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search by City, Zip, Facility Name'}))
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), empty_label="All", required=False)
    facility_type = forms.ModelChoiceField(queryset=FacilityType.objects.all(), empty_label="All", required=False)
    amenities = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(attrs={'id':'id_amenities'}), 
            queryset=Amenity.objects.all(), 
            required=False
    )
    min_value = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=SEARCH_MIN_VAL_INITIAL)
    max_value = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=SEARCH_MAX_VAL_INITIAL)

class ListPropertyForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description'}))

    def send_email(self):
        message = self.cleaned_data['description'] + "<br/>"
        who = self.cleaned_data['first_name']
        send_mail(
                subject="Home For Grandma: Listing Request from" + who,
                message = message + "from: " + who,
                from_email=self.cleaned_data['email'],
                recipient_list = [settings.CONTACT_EMAIL],
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
                recipient_list = [settings.CONTACT_EMAIL],
                )
             

class TourRequestForm(FacilityMessageFormFieldMixin, ModelForm):
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':"Can you describe the health of the resident?", 'cols':"27"}),
        required=False
    )
    move_in_time_frame = forms.ChoiceField(
        choices=field_choices_empty['move_in_time_frame'], 
        required=False
    )
    care_mobility = forms.ChoiceField(
        choices=field_choices_empty['mobility'], 
        required=False
    )
    care_current = forms.ChoiceField(
        choices=field_choices_empty['care_current'], 
        required=False
    )
    health_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':"Describe your health condition", 'cols':"27"}),
        required=False
    )
    desired_city = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':"Desired City"}),
        required=False
    )

    class Meta:
        model = FacilityMessage
        exclude = ('user','facility','read_by_manager','read_by_provider','replied_by','replied_datetime')
        widgets = {
            'planned_move_date': forms.TextInput(attrs={'placeholder': 'Planned move-in Time Frame', 'class':''}),
        }
    
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
            
MAX_FEATURED_FACILITIES = 6

class FacilityAdminForm(ModelForm):
    holding_group = make_ajax_field(Facility, 'holding_group', 'holding_group', help_text=None)

    class Meta:
        model = Facility
        widgets = {
            'description_long':forms.Textarea,
        }

    def clean_phone(self):
        data = self.cleaned_data['phone']
        numbers = re.findall('\d', data)
        number = ''.join(str(s) for s in numbers)
        if not len(number) == 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")
        return number

    def clean_shown_on_home(self):
        shown_on_home = self.cleaned_data['shown_on_home']
        if (shown_on_home and self.instance and not self.instance.shown_on_home) or (shown_on_home and not self.instance):
            featured_facilities = Facility.objects.filter(shown_on_home=True)
            if len(featured_facilities) >= MAX_FEATURED_FACILITIES:
                raise forms.ValidationError("There are already {0} featured facilities. Remove one before adding another".format(str(MAX_FEATURED_FACILITIES)))
        return shown_on_home


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

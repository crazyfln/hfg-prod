import datetime
import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets
from django.forms.models import BaseInlineFormSet
from django.forms.extras.widgets import SelectDateWidget

from django.utils.translation import ugettext_lazy as _
from ajax_select import make_ajax_field
from pygeocoder import Geocoder

from .models import *
from .facility_message_mixin import field_choices, field_choices_empty, FacilityMessageFormFieldMixin
from account.forms import CustomModelMultipleChoiceField
SEARCH_MIN_VAL_INITIAL = "1000"
SEARCH_MAX_VAL_INITIAL = "9000"

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='search', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search by City, Zip, Community Name', 'autofocus':'autofocus' }))
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), empty_label="All", required=False)
    facility_type = forms.ModelChoiceField(queryset=FacilityType.objects.all(), empty_label="All", required=False)
    amenities = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'id':'id_amenities'}), 
        queryset=Amenity.objects.all(), 
        required=False
    )
    show_map = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'id':'myonoffswitch','class':'onoffswitch-checkbox'}),
        initial=True,
        required=False
    )
    min_value = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=SEARCH_MIN_VAL_INITIAL)
    max_value = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=SEARCH_MAX_VAL_INITIAL)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['show_map'].initial = True

class ListPropertyForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    phone_num = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Phone Number'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description'}))


    def send_email(self):
       
        who_first = self.cleaned_data['first_name']
        who_last = self.cleaned_data['last_name']
        num = self.cleaned_data['phone_num']
        message = self.cleaned_data['description']
        send_mail(
                subject= "Home For Grandma: Listing Request from " + who_first,
                message = "Message: " + message + "\n" + "From: " + who_first + " " + who_last + "\n" + num,
                from_email = self.cleaned_data['email'],
                recipient_list = [settings.CONTACT_EMAIL],
                )

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    contact_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))

    def send_email(self):
        message = self.cleaned_data['message']
        who = self.cleaned_data['name']
        phone = self.cleaned_data['contact_phone']
        send_mail(
                subject = "Home For Grandma: contact us message from " + who,
                message = "Message: " + message + "\n" + "From: " + who + "\n" + "Phone: " + phone, 
                from_email = self.cleaned_data['email'],
                recipient_list = [settings.CONTACT_EMAIL],
                )
             

class TourRequestForm(FacilityMessageFormFieldMixin, ModelForm):
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':"Hi, I found your listing on HomeForGrandma.com and would like to schedule a visit. Thanks!", 'cols':"36"}),
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
        widget=forms.Textarea(attrs={'placeholder':"Can you describe the health of the resident?", 'cols':"36"}),
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
    phone = forms.CharField(max_length=20)

    class Meta:
        model = Facility
        widgets = {
            'description_long':forms.Textarea,
        }

    def clean(self):
        cleaned_data = super(FacilityAdminForm, self).clean()
        base_str = "{0}, "
        address = ""
        address_parts = [cleaned_data.get('address'), cleaned_data.get('city'), cleaned_data.get('state'), cleaned_data.get('zipcode')]
        for part in address_parts:
            if part:
                address += base_str.format(part)
        if not address == "":
            error = forms.ValidationError("Google does not recognize your address, city, state or zipcode combination as a valid address")
            try:
                if not Geocoder.geocode(address).valid_address:
                    raise error
            except:
                raise error

        return cleaned_data

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

class FacilityImageInlineFormset(forms.models.BaseInlineFormSet):
    '''
    validates facility message formset data, specifically to make sure only one is featured.
    '''
    def clean(self):
        super(FacilityImageInlineFormset, self).clean()
        featured = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            featured += 1 if data.get('featured') else 0
        if featured > 1:
            raise ValidationError(_('More than 1 of your the facility images are featured. You may only have 1 featured image.'))
        #elif featured == 0:
        #    raise ValidationError(_('None of the facility images are featured, you must have a featured image'))

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

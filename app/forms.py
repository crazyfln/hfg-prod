import datetime
import re

from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm, widgets
from django.forms.models import BaseInlineFormSet
from django.forms.extras.widgets import SelectDateWidget

from django.utils.translation import ugettext_lazy as _

from .models import *

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all(), empty_label="All", required=False)
    facility_type = forms.ModelChoiceField(queryset=FacilityType.objects.all(), empty_label="All", required=False)
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), required=False)
    min_value = forms.IntegerField(widget=forms.HiddenInput())
    max_value = forms.IntegerField(widget=forms.HiddenInput())#initial value set in __init__

    def __init__(self, *args, **kwargs):
        arguments = args[0].copy()
        arguments.setdefault('min_value',149)
        arguments.setdefault('max_value',3500)
        super(SearchForm, self).__init__(arguments, **kwargs)

class StripeTokenForm(forms.Form):
    id = forms.CharField()


class ChargeForm(forms.Form):
    amount = forms.DecimalField(max_digits=5, decimal_places=2)

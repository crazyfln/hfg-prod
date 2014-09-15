from django.db import models
from model_utils import Choices
from django import forms

SEARCHING_FOR_CHOICES = Choices('Myself', 'Family', 'Friend', 'Client', 'Other',)
BUDGET_CHOICES = Choices('$ 1000', '$ 2000', '$ 3000 Plus', 'Not Sure')
MOBILITY_CHOICES = Choices('Mobile', 'Immobile')
CARE_CURRENT_CHOICES = Choices('Alone', 'With Family')
MOVE_IN_TIME_FRAME_CHOICES = Choices('Now', 'Soon', 'Later') 
PREFERRED_CONTACT_CHOICES = Choices('Phone','Email','Both')

field_choices = {'searching_for':SEARCHING_FOR_CHOICES, 'budget':BUDGET_CHOICES, 'mobility':MOBILITY_CHOICES, 'care_current': CARE_CURRENT_CHOICES, 'move_in_time_frame':MOVE_IN_TIME_FRAME_CHOICES, 'preferred_contact': PREFERRED_CONTACT_CHOICES}

BUDGET_CHOICES_EMPTY = [('','Budget')] + BUDGET_CHOICES
MOBILITY_CHOICES_EMPTY = [('','Mobility')] + MOBILITY_CHOICES
CARE_CURRENT_CHOICES_EMPTY = [('','Current Living Situation')] + CARE_CURRENT_CHOICES
MOVE_IN_TIME_FRAME_CHOICES_EMPTY = [('','Planned move-in Time Frame')] + MOVE_IN_TIME_FRAME_CHOICES
SEARCHING_FOR_CHOICES_EMPTY = [('','I%cm Searching for...' %39)] + SEARCHING_FOR_CHOICES

field_choices_empty = {'budget': BUDGET_CHOICES_EMPTY,'mobility':MOBILITY_CHOICES_EMPTY, 'care_current':CARE_CURRENT_CHOICES_EMPTY, 'move_in_time_frame':MOVE_IN_TIME_FRAME_CHOICES_EMPTY, 'searching_for': SEARCHING_FOR_CHOICES_EMPTY}

class FacilityMessageModelFieldMixin(models.Model):
    searching_for = models.CharField(max_length=30, blank=True, choices=field_choices['searching_for'])
    budget = models.CharField(max_length=30, blank=True, choices=field_choices['budget'])
    pay_private_pay = models.BooleanField(default=False, blank=True)
    pay_longterm_care = models.BooleanField(default=False, blank=True)
    pay_veterans_benefits = models.BooleanField(default=False, blank=True)
    pay_medicare = models.BooleanField(default=False, blank=True)
    pay_medicaid = models.BooleanField(default=False, blank=True)
    pay_ssi = models.BooleanField(default=False, blank=True)
    care_bathing = models.BooleanField(default=False, blank=True)
    care_diabetic = models.BooleanField(default=False, blank=True)
    care_mobility = models.CharField(max_length=30, blank=True, choices=MOBILITY_CHOICES)
    care_current = models.CharField(max_length=30, blank=True, choices=CARE_CURRENT_CHOICES)
    care_medical_assistance = models.BooleanField(default=False, blank=True)
    care_toileting = models.BooleanField(default=False, blank=True)
    care_memory_issues = models.BooleanField(default=False, blank=True)
    care_diagnosed_memory = models.BooleanField(default=False, blank=True)
    care_combinative = models.BooleanField(default=False, blank=True)
    care_wandering = models.BooleanField(default=False, blank=True)
    desired_city = models.CharField(max_length=30, blank=True)
    resident_first_name = models.CharField(max_length=30, blank=True)
    health_description = models.CharField(max_length=500, blank=True)
    planned_move_date = models.DateField(blank=True, null=True)
    move_in_time_frame = models.CharField(max_length=30, blank=True, choices=MOVE_IN_TIME_FRAME_CHOICES)
    preferred_contact = models.CharField(max_length=10, blank=True, null=True, choices=PREFERRED_CONTACT_CHOICES)

    class Meta:
        abstract = True

class FacilityMessageFormFieldMixin(forms.ModelForm):
    budget = forms.ChoiceField(
        choices=field_choices['budget'], 
        widget=forms.RadioSelect(attrs={'id':'id_budget'}), 
        required=False
    ) 
    searching_for = forms.ChoiceField(
        choices=field_choices_empty['searching_for'], 
        required=False
    )
    preferred_contact = forms.ChoiceField(
        choices=field_choices['preferred_contact'], 
        widget=forms.RadioSelect(attrs={'id':'id_preferred_contact'}), 
        required=False
    )
    resident_first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':"Resident's First Name"}),
        required=False
    )
    health_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':"Describe your health condition", 'cols':"27"}),
        required=False
    )

    comments = forms.CharField(
            widget=forms.Textarea(attrs={'placeholder':"Hi, I found your listing on HomeForGrandma.com and would like to schedule a visit. Thanks!", 'cols':"27"}),
        required=False
    )

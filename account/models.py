from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
# Create your models here.

from hfg import settings


SEARCHING_FOR_CHOICES = Choices('Myself', 'Family', 'Friend', 'Client', 'Other',)
BUDGET_CHOICES = Choices('1000', '2000', '3000', 'Not Sure')
MOBILITY_CHOICES = Choices('Mobile', 'Immobile')
CARE_CURRENT_CHOICES = Choices('Alone', 'With Family')
MOVE_IN_TIME_FRAME_CHOICES = Choices('Now', 'Soon', 'Later') 


class User(AbstractUser, TimeStampedModel):
    
    phone = models.CharField(max_length=10)
    searching_for = models.CharField(max_length=30, blank=True, choices=SEARCHING_FOR_CHOICES)
    budget = models.CharField(max_length=30, blank=True, choices=BUDGET_CHOICES)

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
    planned_move_date = models.DateTimeField(blank=True, null=True)
    move_in_time_frame = models.CharField(max_length=30, blank=True, choices=MOVE_IN_TIME_FRAME_CHOICES)
    holding_group = models.ForeignKey('HoldingGroup', related_name="owners", null=True,blank=True)

    def is_provider(self):
        return bool(self.holding_group)

    def __unicode__(self):
        if self.get_full_name() == "":
            return self.email
        else:
            return super(User, self).__unicode__()


    def get_absolute_url():
        """
        The absolute url of the user model
        """

        raise NotImplemented()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Account Management"


class HoldingGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


from django.db import models

from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
# Create your models here.

from hfg import settings

class User(AbstractUser, TimeStampedModel):
    
    phone = models.CharField(max_length=10)
    searching_for = models.CharField(max_length=30, blank=True, choices=(
                                    ('Myself','Myself'),
                                    ('Family','Family'),
                                    ('Friend','Friend'),
                                    ('Client','Client'),
                                    ('Other','Other'))
                                    )
    budget = models.CharField(max_length=30, blank=True, choices=(
                                ('1000','1000'),
                                ('2000','2000'),
                                ('3000','3000'),
                                ('Not Sure','Not Sure'))
                                )
    conditions = models.ManyToManyField('app.Condition', blank=True, related_name="users")

    pay_private_pay = models.BooleanField(default=False)
    pay_longterm_care = models.BooleanField(default=False)
    pay_veterans_benefits = models.BooleanField(default=False)
    pay_medicare = models.BooleanField(default=False)
    pay_medicaid = models.BooleanField(default=False)
    pay_ssi = models.BooleanField(default=False)

    care_bathing = models.BooleanField(default=False)
    care_diabetic = models.BooleanField(default=False)
    care_mobility = models.CharField(max_length=30, blank=True, choices=(
                                    ('Mobile','Mobile'),
                                    ('Immobile','Immobile'))
                                    )
    care_current = models.CharField(max_length=30, blank=True, choices=(
                                    ('Alone','Alone'),
                                    ('With Family','With Family'))
                                    )
    care_medical_assistance = models.BooleanField(default=False)
    care_toileting = models.BooleanField(default=False)
    care_memory_issues = models.BooleanField(default=False)
    care_diagnosed_memory = models.BooleanField(default=False)
    care_combinative = models.BooleanField(default=False)
    care_wandering = models.BooleanField(default=False)
    desired_city = models.CharField(max_length=30, blank=True)
    resident_first_name = models.CharField(max_length=30, blank=True)
    health_description = models.CharField(max_length=500, blank=True)
    planned_move_date = models.DateTimeField(blank=True, null=True)
    move_in_time_frame = models.CharField(max_length=30, blank=True, choices=(
                                        ('Now','Now'),
                                        ('Soon','Soon'),
                                        ('Later','Later'))
                                        ) 


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



class HoldingGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class FacilityDirector(User):
    holding_group = models.ForeignKey(HoldingGroup, related_name="owners")

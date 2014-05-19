from django.db import models

from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
# Create your models here.

from hfg import settings

class User(AbstractUser, TimeStampedModel):

    #custom user fields go here
    ####
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

class FacilityDirector(User):
    phone = models.IntegerField()
    holding_group = models.ForeignKey(HoldingGroup, related_name="owners")

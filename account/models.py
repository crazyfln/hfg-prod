from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
# Create your models here.

from hfg import settings
from app.facility_message_mixin import FacilityMessageModelFieldMixin




class User(AbstractUser, TimeStampedModel, FacilityMessageModelFieldMixin):
    
    phone = models.CharField(max_length=10)
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


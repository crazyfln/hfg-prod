from django.db import models

from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
# Create your models here.

from hfg import settings

class User(AbstractUser, TimeStampedModel):
    
    phone = models.CharField(max_length=10)
    searching_for = models.CharField(max_length=30, choices=(
                                    ('Myself','Myself'),
                                    ('Family','Family'),
                                    ('Friend','Friend'),
                                    ('Client','Client'),
                                    ('Other','Other'))
                                    )
    budget = models.CharField(max_length=30, choices=(
                                ('1000','1000'),
                                ('2000','2000'),
                                ('3000','3000'),
                                ('Not Sure','Not Sure'))
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

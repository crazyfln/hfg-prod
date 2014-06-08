from django.db import models

from model_utils.models import TimeStampedModel
from django_extensions.db.models import AutoSlugField
from django.core.urlresolvers import reverse

from account.models import User, FacilityDirector, HoldingGroup

class Facility(TimeStampedModel):
    name = models.CharField(max_length=50)
    favorited_by = models.ManyToManyField(User, through='Favorite', related_name="favorites")
    facility_types = models.ManyToManyField('FacilityType')
    holding_group = models.ForeignKey(HoldingGroup)
    director_name = models.CharField(max_length=50)
    director_email = models.EmailField(max_length=100)
    director_avatar = models.ImageField(upload_to=
                                        lambda instance, filename: 'director_avatars/' + str(instance.name.replace(' ','_')) + '/')
    phone = models.CharField(max_length=10)
    license = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    min_price = models.IntegerField()
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    slug = AutoSlugField(populate_from=['name', 'zipcode'])
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    shown_on_home = models.BooleanField()
    status = models.CharField(max_length="20", choices=(
                              ('Vacancies','Vacancies'),
                              ('No Vacancies','No Vacancies'),
                              ('Dormant', 'Dormant'), # think dormant is being removed
                              ))
    description_short = models.CharField(max_length=140)
    description_long = models.CharField(max_length=1000)
       
    care_level_1_cost = models.IntegerField()
    care_level_2_cost = models.IntegerField()
    care_level_3_cost = models.IntegerField()
    care_memory_cost = models.IntegerField()
    medication_level_1_cost = models.IntegerField()
    medication_level_2_cost = models.IntegerField()
    medication_level_3_cost = models.IntegerField()
    capacity = models.IntegerField()
    vacancies = models.IntegerField()
    
    languages = models.ManyToManyField('Language', related_name="facilities")
    conditions = models.ManyToManyField('Condition', related_name="facilities")
    amenities = models.ManyToManyField('Amenity', related_name="facilities")
    fees = models.ManyToManyField('Fee', through="FacilityFee")
    care_type = models.CharField(max_length="20", choices=(
                                   ("Rent Only","Rent Only"),
                                   ("Rent and Care","Rent and Care"),
                                   ))
    phone_requested_by = models.ManyToManyField(User, through="PhoneRequest", related_name="phone_requests")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('facility_details', args=(self.slug,))

class FacilityFee(TimeStampedModel):
    facility = models.ForeignKey(Facility)
    fee = models.ForeignKey('Fee')
    cost = models.IntegerField()

    def __unicode__(self):
        return self.facility.name + "-" + self.fee.name

class Fee(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
    
class FacilityMessage(TimeStampedModel):
    user = models.ForeignKey(User)
    #<health detail fields>
    read = models.BooleanField(default=False)
    replied_by = models.CharField(max_length=20)
    replied_datetime = models.DateTimeField()

class FacilityType(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Language(TimeStampedModel):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name
    
class Condition(TimeStampedModel):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name
    
class Amenity(TimeStampedModel):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class RoomType(TimeStampedModel):
    facility = models.ForeignKey(Facility, related_name="room_types")
    unit_type = models.CharField(max_length="20", choices=(
                                   ("small room","small room"),
                                   ("big room","big room"),
                                   ))
    square_footage = models.CharField(max_length="20", choices=(
                                   ("20 x 50","20 x 50"),
                                   ("100 x 50","100 x 50"),
                                   ))
    starting_price = models.DecimalField(max_digits=15, decimal_places=2)


    def __unicode__(self):
        return str(self.facility) + "-" + self.unit_type +":"+ str(self.starting_price)
    

class FacilityImage(TimeStampedModel):
    facility = models.ForeignKey(Facility, related_name="images")
    featured = models.BooleanField()
    image = models.ImageField(upload_to='facility_images/' + str(facility) + '/')

class Inquiry(TimeStampedModel):
    from_user = models.ForeignKey(User)
    est_move = models.DateField()
    message = models.CharField(max_length=300)
    remind = models.BooleanField()

class Invoice(TimeStampedModel):
    holding_group = models.ForeignKey(HoldingGroup) #if we dropped holding group and just had FK with facility, we could get the holding group of the facility right?
    facility = models.ForeignKey(Facility) 
    status = models.CharField(max_length="20", choices=(
                                   ("paid","paid"),
                                   ("unpaid","unpaid"),
                                   ))
    payment_method = models.CharField(max_length="20", choices=(
                                   ("credit","credit"),
                                   ("check","check"),
                                   ))
    #billed_on = created_on ??
    contact_person_name = models.CharField(max_length=50)
    contact_person_relationship = models.CharField(max_length=100)
    contact_person_phone = models.IntegerField()
    contact_person_email = models.EmailField()
    move_in_date = models.DateTimeField()
    resident_name = models.CharField(max_length=50)
    amount = models.IntegerField()

class Favorite(TimeStampedModel):
    user = models.ForeignKey(User)
    facility = models.ForeignKey(Facility)

class PhoneRequest(TimeStampedModel):
    user = models.ForeignKey(User)
    facility = models.ForeignKey(Facility)
    
    def __unicode__(self):
        return str(self.facility) + ":" + str(self.user.get_full_name) + " at: " + str(self.created)

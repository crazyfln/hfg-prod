from django.db import models

from model_utils.models import TimeStampedModel
from django_extensions.db.models import AutoSlugField
from django.core.urlresolvers import reverse

from account.models import User, FacilityDirector, HoldingGroup

from util.util import file_url

class Facility(TimeStampedModel):
    name = models.CharField(max_length=50)
    favorited_by = models.ManyToManyField(User, through='Favorite', related_name="favorites")
    facility_types = models.ManyToManyField('FacilityType')
    holding_group = models.ForeignKey('account.HoldingGroup')
    director_name = models.CharField(max_length=50)
    director_email = models.EmailField(max_length=100)
    director_avatar = models.ImageField(upload_to=file_url("facility_director_images"))
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
    shown_on_home = models.BooleanField(default=False)
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
    rooms = models.ManyToManyField('RoomType', through='FacilityRoom')
    care_type = models.CharField(max_length="20", choices=(
                                   ("Rent Only","Rent Only"),
                                   ("Rent and Care","Rent and Care"),
                                   ))
    phone_requested_by = models.ManyToManyField(User, through="PhoneRequest", related_name="phone_requests")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('facility_details', args=(self.slug,))

    def get_phone_parts(self):
        number_parts = []
        number_parts.append(self.phone[:3])
        number_parts.append(self.phone[3:6])
        number_parts.append(self.phone[6:])
        return number_parts

    def get_phone_stars(self,):
        parts = self.get_phone_parts()
        return "(" + parts[0] + ") " + parts[1] + "-****"

    def get_phone_normal(self):
        parts = self.get_phone_parts()
        return "(" + parts[0] + ") " + parts[1] + "-" + parts[2]

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

BUDGET_CHOICES = [
    ('1000','1000'),
    ('2000','2000'),
    ('3000','3000'),
    ('Not Sure','Not Sure')
]
CARE_MOBILITY_CHOICES = [
    ('Mobile','Mobile'),
    ('Immobile','Immobile')
]
CARE_CURRENT_CHOICES = [
    ('Alone','Alone'),
    ('With Family','With Family')
]
MOVE_IN_TIME_FRAME_CHOICES = [
    ('Now','Now'),
    ('Soon','Soon'),
    ('Later','Later')
]
SEARCHING_FOR_CHOICES = [
    ('Myself','Myself'),
    ('Family','Family'),
    ('Friend','Friend'),
    ('Client','Client'),
    ('Other','Other')
]
class FacilityMessage(TimeStampedModel):
    user = models.ForeignKey(User)
    facility = models.ForeignKey(Facility)
    budget = models.CharField(max_length=30, blank=True, choices=BUDGET_CHOICES)

    pay_private_pay = models.BooleanField()
    pay_longterm_care = models.BooleanField()
    pay_veterans_benefits = models.BooleanField()
    pay_medicare = models.BooleanField()
    pay_medicaid = models.BooleanField()
    pay_ssi = models.BooleanField()

    care_bathing = models.BooleanField()
    care_diabetic = models.BooleanField()
    care_mobility = models.CharField(max_length=30, blank=True, choices=CARE_MOBILITY_CHOICES)

    care_current = models.CharField(max_length=30, blank=True, choices=CARE_CURRENT_CHOICES)

    care_medical_assistance = models.BooleanField()
    care_toileting = models.BooleanField()
    care_memory_issues = models.BooleanField()
    care_diagnosed_memory = models.BooleanField()
    care_combinative = models.BooleanField()
    care_wandering = models.BooleanField()

    comments = models.CharField(max_length=500, blank=True)
    health_description = models.CharField(max_length=500, blank=True)
    planned_move_date = models.DateTimeField(blank=True, null=True)
    move_in_time_frame = models.CharField(max_length=30, blank=True, choices=MOVE_IN_TIME_FRAME_CHOICES)

    desired_city = models.CharField(max_length=30, blank=True)
    searching_for = models.CharField(max_length=30, blank=True, choices=SEARCHING_FOR_CHOICES)

    resident_first_name = models.CharField(max_length=30, blank=True)

    read = models.BooleanField(default=False)
    replied_by = models.CharField(max_length=20, blank=True)
    replied_datetime = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(FacilityMessage, self).save(*args, **kwargs)
        user = self.user
        for field in self._meta.get_all_field_names():
            if field in ["id","created","modified"]:
                continue
            elif hasattr(user, field):
                setattr(user, field, getattr(self, field))
        user.save()


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
    users = models.ManyToManyField('account.User', blank=True, related_name="conditions")
    def __unicode__(self):
        return self.name

class Amenity(TimeStampedModel):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class FacilityRoom(TimeStampedModel):
    facility = models.ForeignKey(Facility)
    room_type = models.ForeignKey('RoomType')
    width = models.CharField(max_length=5)
    length = models.CharField(max_length=5)
    starting_price = models.DecimalField(max_digits=15, decimal_places=2)

    def get_square_footage(self):
        return self.width + ' x ' + self.length

    def __unicode__(self):
        return str(self.facility) + '-' + str(self.room_type) + '-' + self.pk

class RoomType(TimeStampedModel):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class FacilityImage(TimeStampedModel):
    facility = models.ForeignKey(Facility, related_name="images")
    featured = models.BooleanField()
    image = models.ImageField(upload_to=file_url("facility_images"))

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

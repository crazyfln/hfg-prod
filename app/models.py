from django.db import models

from model_utils.models import TimeStampedModel
from django_extensions.db.models import AutoSlugField
from django.core.urlresolvers import reverse

from account.models import User, HoldingGroup

from util.util import file_url
from .facility_message_mixin import FacilityMessageModelFieldMixin
from urllib import quote_plus 

class Facility(TimeStampedModel):
    name = models.CharField(max_length=50)
    favorited_by = models.ManyToManyField(User, through='Favorite', related_name="favorites", blank=True)
    facility_types = models.ManyToManyField('FacilityType', blank=True)
    holding_group = models.ForeignKey('account.HoldingGroup', blank=True, null=True)
    director_name = models.CharField(max_length=50, blank=True)
    director_email = models.EmailField(max_length=100, blank=True)
    director_avatar = models.ImageField(upload_to=file_url("facility_director_images"), blank=True)
    phone = models.CharField(max_length=10, blank=True)
    license = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    min_price = models.IntegerField(default=0, blank=True)
    address = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    slug = AutoSlugField(populate_from=['name', 'zipcode'])
    latitude = models.IntegerField(blank=True, default=0)
    longitude = models.IntegerField(blank=True, default=0)
    shown_on_home = models.BooleanField(default=False)
    description_short = models.CharField(max_length=140, blank=True)
    description_long = models.CharField(max_length=1000, blank=True)

    care_level_1_cost = models.IntegerField(default=0)
    care_level_2_cost = models.IntegerField(default=0)
    care_level_3_cost = models.IntegerField(default=0)
    care_memory_cost = models.IntegerField(default=0)
    medication_level_1_cost = models.IntegerField(default=0)
    medication_level_2_cost = models.IntegerField(default=0)
    medication_level_3_cost = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    vacancies = models.IntegerField(default=0)

    languages = models.ManyToManyField('Language', related_name="facilities", blank=True)
    conditions = models.ManyToManyField('Condition', related_name="facilities", blank=True)
    amenities = models.ManyToManyField('Amenity', related_name="facilities", blank=True)
    fees = models.ManyToManyField('Fee', through="FacilityFee", blank=True)
    rooms = models.ManyToManyField('RoomType', through='FacilityRoom', blank=True)
    care_type = models.CharField(max_length="20", choices=(
                                   ("Rent Only","Rent Only"),
                                   ("Rent and Care","Rent and Care"),
                                   ))
    phone_requested_by = models.ManyToManyField(User, through="PhoneRequest", related_name="phone_requests", blank=True)
    visibility = models.BooleanField(default=True)
    manager_note = models.CharField(max_length=1000, blank=True, null=True)



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

    def get_director_avatar_url(self):
        if self.director_avatar:
            return self.director_avatar.url
        else:
            return ""

    def get_phone_stars(self,):
        if self.phone:
            parts = self.get_phone_parts()
            return "(" + parts[0] + ") " + parts[1] + "-****"
        else:
            return None

    def get_phone_normal(self):
        if self.phone:
            parts = self.get_phone_parts()
            return "(" + parts[0] + ") " + parts[1] + "-" + parts[2]
        else:
            return None

    def get_featured_image(self):
        return self.images.get(featured = True)

    def get_vacancy_status(self):
        return "Vacancies" if self.vacancies > 0 else "No Vacancies"

    def get_encoded_address(self):
        return quote_plus(",".join([self.address, self.city, self.state, self.zipcode]))


    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Listing Management"



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

    class Meta:
        verbose_name_plural = "Types of Additional Fees"

class FacilityMessage(TimeStampedModel, FacilityMessageModelFieldMixin):
    user = models.ForeignKey(User)
    facility = models.ForeignKey(Facility)

    read_by_manager = models.BooleanField(default=False)
    read_by_provider = models.BooleanField(default=False)
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

    def __unicode__(self):
        return "-".join([str(self.facility.name), str(self.user.get_full_name()), str(self.created.date())])

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Message Center"


class FacilityType(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types of Facilities"

class Language(TimeStampedModel):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types of Languages"

class Condition(TimeStampedModel):
    name = models.CharField(max_length=40)
    users = models.ManyToManyField('account.User', blank=True, related_name="conditions")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types of Conditions"

class Amenity(TimeStampedModel):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types of Amenities"

class FacilityRoom(TimeStampedModel):
    facility = models.ForeignKey(Facility)
    room_type = models.ForeignKey('RoomType', blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def get_area(self):
        return str(self.area) + "sqft" if self.area else None
        
    def __unicode__(self):
        return str(self.facility) + '-' + str(self.room_type) + '-' + str(self.pk)

class RoomType(TimeStampedModel):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Types of Rooms"

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
    # dropped holding_group fk since we can get that from the facility
    facility = models.ForeignKey(Facility)
    status = models.CharField(max_length="20", choices=(
                                   ("paid","paid"),
                                   ("unpaid","unpaid"),
                                   ))
    payment_method = models.CharField(max_length="20", choices=(
                                   ("credit","credit"),
                                   ("check","check"),
                                   ))
    billed_on = models.DateTimeField()
    recieved = models.CharField(max_length=10)
    contact_person_name = models.CharField(max_length=50)
    contact_person_relationship = models.CharField(max_length=100)
    contact_person_phone = models.CharField(max_length=10)
    contact_person_email = models.EmailField()
    move_in_date = models.DateTimeField()
    resident_name = models.CharField(max_length=50)
    amount = models.CharField(max_length=15)
    manager_note = models.CharField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return str(self.facility) + "-" + self.resident_name + "-" + str(self.billed_on.date())
    class Meta:
        verbose_name = "Claim"
        verbose_name_plural = "Income Management"

class Favorite(TimeStampedModel):
    user = models.ForeignKey(User)
    facility = models.ForeignKey(Facility)

class PhoneRequest(TimeStampedModel):
    user = models.ForeignKey(User)
    facility = models.ForeignKey(Facility)

    def __unicode__(self):
        return str(self.facility) + ":" + str(self.user.get_full_name) + " at: " + str(self.created)

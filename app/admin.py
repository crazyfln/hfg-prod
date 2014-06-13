from django.contrib import admin
import reversion

from django.forms import CheckboxSelectMultiple
from .models import *

# class YourModelAdmin(reversion.VersionAdmin):
#     pass

class FacilityFeeInline(admin.TabularInline):
    model = FacilityFee
    extra = 1 

class FacilityImageInline(admin.TabularInline):
    model = FacilityImage

class FacilityRoomInline(admin.TabularInline):
    model = FacilityRoom

class FacilityAdmin(admin.ModelAdmin):
    list_display = ['pk','name','created','modified','city','state','holding_group']
    fieldsets = (
        ("Facility Information", {
            'fields':(
                'holding_group', 
                ('name','facility_types','capacity'),
                ('address','vacancies'),
                'director_email',
                ('city','state','zipcode','license','shown_on_home'),
                'description_short',
                'description_long'
                )}),
        ("Community Manager", {
            'fields':(
                ('director_name','director_avatar')
                )}),
        ("Add Photos", {
            'fields':(
                )}),
        ("Faciity Information", {
            'fields':(
                ('languages','conditions','amenities')
                )}),
        ("Edit Floor & Service Plans", {
            'fields':(
                ('care_type'),
                ('care_level_1_cost','care_level_2_cost','care_level_3_cost','care_memory_cost'),
                ('medication_level_1_cost','medication_level_2_cost','medication_level_3_cost')
                )})
            )
    list_select_related = True
    inlines = [FacilityFeeInline, FacilityImageInline, FacilityRoomInline]
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
                
admin.site.register(Facility, FacilityAdmin)

class FacilityMessageAdmin(admin.ModelAdmin):
    list_display = ['created','get_holding_group','facility','get_user_full_name', 'comments','replied_by','replied_datetime']

    def get_holding_group(self, obj):
        return obj.facility.holding_group
    get_holding_group.short_description = "Account"

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = "Sender Name"

admin.site.register(FacilityMessage, FacilityMessageAdmin)


admin.site.register(FacilityType)
admin.site.register(Fee)
admin.site.register(FacilityFee)
admin.site.register(Language)
admin.site.register(Condition)
admin.site.register(Amenity)
admin.site.register(RoomType)
admin.site.register(FacilityImage)

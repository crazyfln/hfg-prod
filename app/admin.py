from django.contrib import admin
import reversion

from django.forms import CheckboxSelectMultiple
from .models import *
from .forms import FacilityAdminForm

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
    form = FacilityAdminForm
    list_display = ['edit','note','delete','pk','name','created','modified','city','state','holding_group']
    fieldsets = (
        ("Facility Information", {
            'fields':(
                'holding_group', 
                ('name','facility_types','capacity'),
                ('address','vacancies'),
                'director_email',
                ('city','state','zipcode'),
                ('license','shown_on_home'),
                'description_short',
                'description_long'
                )}),
        ("Community Manager", {
            'fields':(
                ('director_name','director_avatar')
                )}),
        ("Fields not in wires", {
            'fields':(
                'min_price',
                'latitude',
                'longitude',
                'phone'
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

    
    def edit(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:%s_%s_change' % info, args=(obj.id,))
        return "<a href='%s'>Edit</a>" % url
    edit.allow_tags = True
    
    def note(self, obj):
        return "note"

    def delete(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:%s_%s_delete' % info, args=(obj.id,))
        return "<a href='%s'>Delete</a>" % url
    delete.allow_tags = True
                
admin.site.register(Facility, FacilityAdmin)

class FacilityMessageAdmin(admin.ModelAdmin):
    list_display = ['created','get_holding_group','facility','get_user_full_name', 'message','replied_by','replied_datetime']

    def message(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:{0}_{1}_change'.format(info, args=(obj.id,)))
        comment_display = obj.comments[:20]
        return "<a href='{0}'>{1}</a>".format(url, comment_display)
    message.allow_tags = True


    def get_holding_group(self, obj):
        return obj.facility.holding_group
    get_holding_group.short_description = "Account"

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = "Sender Name"

admin.site.register(FacilityMessage, FacilityMessageAdmin)

admin.site.register(FacilityType)
admin.site.register(Fee)
admin.site.register(Language)
admin.site.register(Condition)
admin.site.register(Amenity)
admin.site.register(RoomType)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['edit','note','delete','pk','facility','billed_on','get_recieved','status','payment_method']
    fieldsets = (
        (None, {
            'fields':(
                'facility',
                ('billed_on','recieved'),
                ('status','payment_method'),
                ('resident_name','move_in_date'),
                ('contact_person_name','contact_person_relationship'),
                ('contact_person_phone', 'contact_person_email')
            )
        }),
    )

    def get_recieved(self, obj):
        return "$"+obj.recieved
    get_recieved.short_description = "recieved"

    def edit(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:%s_%s_change' % info, args=(obj.id,))
        return "<a href='%s'>Edit</a>" % url
    edit.allow_tags = True
    
    def note(self, obj):
        return "note"

    def delete(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:%s_%s_delete' % info, args=(obj.id,))
        return "<a href='%s'>Delete</a>" % url
    delete.allow_tags = True
admin.site.register(Invoice, InvoiceAdmin)


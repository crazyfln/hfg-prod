from django.contrib import admin
from django.contrib.admin.sites import AdminSite
import reversion

from django.forms import CheckboxSelectMultiple
from account.models import User, HoldingGroup
from account.admin import UserAdmin
from util.util import list_button
from .models import *
from .forms import FacilityAdminForm

# class YourModelAdmin(reversion.VersionAdmin):
#     pass

class ManagerAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_superuser

manager_admin = ManagerAdmin(name="manager_admin")

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
        return list_button(self, obj, "change", "Edit")
    edit.allow_tags = True
    
    def note(self, obj):
        return "note"

    def delete(self, obj):
        return list_button(self, obj,"delete","Delete")
    delete.allow_tags = True
                
manager_admin.register(Facility, FacilityAdmin)

class FacilityMessageAdmin(admin.ModelAdmin):
    list_display = ['created','get_holding_group','facility','get_user_full_name', 'message','replied_by','replied_datetime']

    def message(self, obj):
        return list_button(self,obj,"change", obj.comments[:20])
    message.allow_tags = True


    def get_holding_group(self, obj):
        return obj.facility.holding_group
    get_holding_group.short_description = "Account"

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = "Sender Name"

manager_admin.register(FacilityMessage, FacilityMessageAdmin)

#admin.site.register(FacilityType)
#admin.site.register(Fee)
#admin.site.register(Language)
#admin.site.register(Condition)
#admin.site.register(Amenity)
#admin.site.register(RoomType)

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
        return list_button(self,obj,"change","Edit")
    edit.allow_tags = True
    
    def note(self, obj):
        return "note"

    def delete(self, obj):
        return list_button(self,obj,"delete","Delete")
    delete.allow_tags = True

manager_admin.register(Invoice, InvoiceAdmin)
manager_admin.register(User, UserAdmin)
manager_admin.register(HoldingGroup)
## PROVIDER ADMIN ##

class ProviderAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_provider()

provider_admin = ProviderAdmin(name="provider_admin")

class FacilityProviderProxy(Facility):
    class Meta:
        proxy = True

class FacilityProviderAdmin(FacilityAdmin):
    list_display = ['edit','delete','pk','name','status','get_messages','get_visibility']

    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_provider()

    def has_change_permission(self, request, obj=None):
        if obj and obj.holding_group != request.user.holding_group:
            return False
        return request.user.is_active and request.user.is_staff and request.user.is_provider()

    def get_messages(self, obj):
        return "not implemented"
    get_messages.short_description = "Messages"

    def get_visibility(self, obj):
        return "not implemented"
    get_visibility.short_description = "Visibility"

    def edit(self, obj):
        return list_button(self,obj,"change","Edit")
    edit.allow_tags = True

    def delete(self, obj):
        return list_button(self,obj,"delete","Delete")
    delete.allow_tags = True

    def queryset(self, request):
        query = super(FacilityProviderAdmin, self).queryset(request)
        return query.filter(holding_group=request.user.holding_group)

provider_admin.register(FacilityProviderProxy, FacilityProviderAdmin)

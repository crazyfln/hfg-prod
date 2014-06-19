from django.contrib import admin
from django.contrib.admin.sites import AdminSite
import reversion
from django.shortcuts import get_object_or_404

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

class FacilityAdmin(EditButtonMixin, NoteButtonMixin, DeleteButtonMixin, admin.ModelAdmin):
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

manager_admin.register(Facility, FacilityAdmin)

class FacilityMessageAdmin(admin.ModelAdmin):
    list_display = ['created','get_holding_group','facility','get_user_full_name', 'message','get_replied']

    def message(self, obj):
        return list_button(self,obj,"change", obj.comments[:20])
    message.allow_tags = True

    def get_replied(self, obj):
        if obj and not obj.replied_by and not obj.replied_datetime:
            return "-"
        return str(obj.replied_by) + "-" + str(obj.replied_datetime.date())
    get_replied.short_description = "Sent to Facility"

    def get_holding_group(self, obj):
        return obj.facility.holding_group
    get_holding_group.short_description = "Account"

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = "Sender Name"

manager_admin.register(FacilityMessage, FacilityMessageAdmin)

class InvoiceAdmin(EditButtonMixin, NoteButtonMixin, DeleteButtonMixin, admin.ModelAdmin):
    list_display = ['edit','note','delete','pk','facility','billed_on','get_amount','get_recieved','status','payment_method']
    fieldsets = (
        (None, {
            'fields':(
                'facility',
                ('amount','recieved'),
                'billed_on',
                ('status','payment_method'),
                ('resident_name','move_in_date'),
                ('contact_person_name','contact_person_relationship'),
                ('contact_person_phone', 'contact_person_email')
            )
        }),
    )

    def get_amount(self, obj):
        return "$" + str(obj.amount)
    get_amount.short_description = "Billed"

    def get_recieved(self, obj):
        return "$"+obj.recieved
    get_recieved.short_description = "Recieved"

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Income Management"

manager_admin.register(Invoice, InvoiceAdmin)
manager_admin.register(User, UserAdmin)
manager_admin.register(HoldingGroup)

## PROVIDER ADMIN ##

class ProviderAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_provider()

provider_admin = ProviderAdmin(name="provider_admin")
class ProviderEditMixin(object):
    def has_change_permission(self, request, obj=None):
        if obj and obj.facility.holding_group != request.user.holding_group:
            return False
        return request.user.is_active and request.user.is_provider() and request.user.is_staff

class ProviderAddMixin(object):
    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_provider()

class FacilityProviderProxy(Facility):
    class Meta:
        proxy = True
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

class FacilityFeeProviderInline(FacilityFeeInline):
    model = FacilityFee
    extra = 1 
    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

class FacilityImageProviderInline(FacilityImageInline):
    model = FacilityImage
    def has_change_permission(self, request, obj=None):
        return True

class FacilityRoomProviderInline(FacilityRoomInline):
    model = FacilityRoom
    def has_change_permission(self, request, obj=None):
        return True

class FacilityProviderAdmin(ProviderAddMixin, ProviderEditMixin, FacilityAdmin):
    list_display = ['edit','delete','pk','name','status','get_messages','get_visibility']
    inlines = [FacilityFeeProviderInline, FacilityImageProviderInline, FacilityRoomProviderInline]


    def get_messages(self, obj):
        msgs = obj.facilitymessage_set.all()
        unread = msgs.filter(read_provider=False)
        display = str(len(msgs)) + " (" + str(len(unread)) + " Unread)"
        meta = FacilityMessageProviderProxy.objects.model._meta
        info = self.admin_site.name, meta.app_label, meta.module_name, "changelist"
        url = reverse('{0}:{1}_{2}_{3}'.format(*info)) + "?q=" + str(obj.slug)
        return "<a href='{0}'>{1}</a>".format(url, display)
    get_messages.allow_tags = True
    get_messages.short_description = "Messages"

    def get_visibility(self, obj):
        return "not implemented"
    get_visibility.short_description = "Visibility"

    def queryset(self, request):
        query = super(FacilityProviderAdmin, self).queryset(request)
        return query.filter(holding_group=request.user.holding_group)

provider_admin.register(FacilityProviderProxy, FacilityProviderAdmin)

class FacilityMessageProviderProxy(FacilityMessage):
    class Meta:
        proxy = True
        verbose_name = "Message"
        verbose_name_plural = "Message Center"

class FacilityMessageProviderAdmin(ProviderEditMixin, FacilityMessageAdmin):
    list_display = ['created','facility','get_user_full_name', 'message','get_replied']

    def queryset(self, request):
        query = super(FacilityMessageProviderAdmin, self).queryset(request)
        if 'q' in request.GET:
            q = request.GET['q']
            facility = get_object_or_404(FacilityProviderProxy, slug=q)
            query = query.filter(facility=facility)
        return query.filter(facility__holding_group=request.user.holding_group)

provider_admin.register(FacilityMessageProviderProxy, FacilityMessageProviderAdmin)

class InvoiceProviderProxy(Invoice):
    class Meta:
        proxy = True
        verbose_name = "Billing Details"
        verbose_name_plural = "Billing History"

class InvoiceProviderAdmin(ProviderEditMixin, InvoiceAdmin):
    list_display = ['facility','billed_on','get_amount','resident_name','move_in_date','get_case_number']

    def get_case_number(self,obj):
        return list_button(self,obj,'change',obj.pk)
    get_case_number.allow_tags = True
    get_case_number.short_description = "Case Number"
    

    def queryset(self, request):
        query = super(InvoiceProviderAdmin, self).queryset(request)
        return query.filter(facility__holding_group=request.user.holding_group)
        

provider_admin.register(InvoiceProviderProxy, InvoiceProviderAdmin)

class EditButtonMixin(object):
    def edit(self, obj):
        return list_button(self,obj,"change","Edit")
    edit.allow_tags = True

class NoteButtonMixin(object):
    def note(self, obj):
        return "note"

class DeleteButtonMixin(object):
    def delete(self, obj):
        return list_button(self,obj,"delete","Delete")
    delete.allow_tags = True

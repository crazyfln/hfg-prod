from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db.models import Q
import reversion
import datetime
import urllib
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.forms import CheckboxSelectMultiple
import datetime
from liststyle.admin import ListStyleAdminMixin

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin

from ajax_select import make_ajax_form
from account.models import User, HoldingGroup
from account.admin import UserAdmin
from util.util import list_button
from .admin_mixins import *
from .models import *
from .forms import FacilityAdminForm, FacilityProviderForm, FacilityImageInlineFormset

class ManagerAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_superuser

manager_admin = ManagerAdmin(name="manager_admin")
manager_admin.register(Entry, EntryAdmin)

class FacilityFeeInline(admin.TabularInline):
    model = FacilityFee
    extra = 1 

class FacilityImageInline(admin.TabularInline):
    model = FacilityImage
    formset = FacilityImageInlineFormset

class FacilityRoomInline(admin.TabularInline):
    model = FacilityRoom


class ShownOnHomeFilter(admin.SimpleListFilter):
    title = _('View Listings Featured on Homepage')
    parameter_name = 'shown_on_home'
    def lookups(self, request, model_admin):
        return (
            ('featured', _('View Featured Listings')),
        )       
                
    def queryset(self, request, queryset):
        if self.value() == 'featured':
            return queryset.filter(shown_on_home=True)

class FacilityAdmin(EditButtonMixin, NoteButtonMixin, DeleteButtonMixin, admin.ModelAdmin):
    form = FacilityAdminForm
    list_display = ['edit','note','delete','pk','name','created','modified','city','state','holding_group', 'get_visibility', 'get_director_email', 'get_min_price']
    list_filter = (ShownOnHomeFilter,)
    search_fields = ['name', 'city', 'state']
    fieldsets = (
        ("Facility Information", {
            'fields':(
                'visibility',
                'holding_group', 
                ('name','facility_types','capacity'),
                ('address','vacancies'),
                'director_email',
                ('city','state'),
                'zipcode',
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

    def get_director_email(self, obj):
        return obj.director_email if obj.director_email else "---"
    get_director_email.short_description = "Email"

    def get_visibility(self, obj):
        display = "Yes" if obj.visibility else "No"
        url = reverse('change_facility_visibility', args=(obj.pk,))
        query = {'admin_site':self.admin_site.name,
            "app_label":obj._meta.app_label,
            "module_name":obj._meta.module_name
        }
        url = url + "?" + urllib.urlencode(query)
        return '<a href="{0}">{1}</a>'.format(url, display)
    get_visibility.short_description = "Published"
    get_visibility.allow_tags = True
    
    def get_min_price(self, obj):
        return "$" + str(obj.min_price) if obj.min_price else "Call"
    get_min_price.short_description = "Price"

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

manager_admin.register(Facility, FacilityAdmin)

class UnreadFilter(admin.SimpleListFilter):
    title = _('View All/Unread/Read')
    parameter_name = 'read_by_manager'
    def lookups(self, request, model_admin):
        return (
            ('unread', _('View Unread Messages Only')),
            ('read', _('View Read Messages Only')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'unread':
            return queryset.filter(read_by_manager=False)
        elif self.value() == 'read':
            return queryset.filter(read_by_manager=True)


class FacilityMessageAdmin(admin.ModelAdmin, ListStyleAdminMixin):
    list_display = ['created','get_holding_group','facility','get_user_full_name', 'message','get_tried_to_call','get_read_by_manager', 'get_replied']
    actions = ['make_read', 'make_unread', 'send_to_facility', 'unsend_to_facility']
    ordering = ['read_by_manager','-modified']
    list_filter = (UnreadFilter,)
    search_fields = ['facility__name', 'facility__holding_group__name']

    def message(self, obj):
        return list_button(self,obj._meta,"change", obj.comments[:20], obj_id=obj.id)
    message.allow_tags = True

    def get_read_by_manager(self, obj):
        return "Read" if obj.read_by_manager else "unread"
    get_read_by_manager.short_description = "read"

    def get_replied(self, obj):
        if obj and not obj.replied_by and not obj.replied_datetime:
            return "-"
        return str(obj.replied_by) + "-" + str(obj.replied_datetime.date())
    get_replied.short_description = "Sent to Facility"

    def get_holding_group(self, obj):
        return obj.facility.holding_group
    get_holding_group.short_description = "Account"

    def get_user_full_name(self, obj):
        meta = User.objects.model._meta
        return list_button(self,meta,'change',obj.user.get_full_name(),obj_id=obj.user.id)
    get_user_full_name.short_description = "Sender Name"
    get_user_full_name.allow_tags = True

    def get_tried_to_call(self, obj):
        phone_request = PhoneRequest.objects.filter(user=obj.user, facility=obj.facility)
        return True if phone_request else False
    get_tried_to_call.short_description = "Tried to call"
    get_tried_to_call.boolean = True

    
    #Actions
    def make_read(self, request, queryset):
        queryset.update(read_by_manager=True)
    make_read.short_description = "Mark messages as read"

    def make_unread(self, request, queryset):
        queryset.update(read_by_manager=False)
    make_unread.short_description = "Mark messages as unread"

    def send_to_facility(self, request, queryset):
        queryset.update(replied_by=request.user.first_name, replied_datetime=datetime.datetime.now())
        message_string = "{0} messages were sent to providers".format(str(len(queryset)))
        self.message_user(request, message_string)
    send_to_facility.short_description = "Send to Facility"

    def unsend_to_facility(self, request, queryset):
        queryset.update(replied_by="", replied_datetime=None)
    unsend_to_facility.short_description = "Unsend messages"

    def queryset(self, request):
        query = super(FacilityMessageAdmin, self).queryset(request)
        return query.order_by('-read_by_manager', 'modified')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        message = get_object_or_404(FacilityMessage, id=object_id)
        if not message.read_by_manager:
            message.read_by_manager = True
            message.save()
        return super(FacilityMessageAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_row_css(self, obj, index):
        if not obj.read_by_manager:
            return 'strong'
        return ''

manager_admin.register(FacilityMessage, FacilityMessageAdmin)

class InvoiceMonthFilter(admin.SimpleListFilter):
    title = _('View Recent Bills')
    parameter_name = 'created'
    def lookups(self, request, model_admin):
        return (
            ('1month', _('View bills created in past month')),
            ('3month', _('View bills created in past 3 months')),
        )

    def queryset(self, request, queryset):
        today = datetime.datetime.now()
        one_month_ago = today - datetime.timedelta(days=30)
        three_months_ago = today - datetime.timedelta(days=90)

        if self.value() == '1month':
            return queryset.filter(created__gte=one_month_ago)
        elif self.value() == '3month':
            return queryset.filter(created__gte=three_months_ago)

class InvoiceAdmin(EditButtonMixin, NoteButtonMixin, DeleteButtonMixin, admin.ModelAdmin):
    list_display = ['edit','note','delete','pk','facility','billed_on','get_amount','get_recieved','status','payment_method']
    list_filter = (InvoiceMonthFilter,)
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
        amount = obj.amount or "0"
        return "$" + amount
    get_amount.short_description = "Billed"

    def get_recieved(self, obj):
        amount = obj.recieved or "0"
        return "$" + amount
    get_recieved.short_description = "Recieved"

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Income Management"

manager_admin.register(Invoice, InvoiceAdmin)
manager_admin.register(FacilityType)
manager_admin.register(RoomType)
manager_admin.register(Fee)
manager_admin.register(Language)
manager_admin.register(Amenity)
manager_admin.register(Condition)
manager_admin.register(User, UserAdmin)
manager_admin.register(HoldingGroup)

## PROVIDER ADMIN ##

class ProviderAdmin(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_provider()

provider_admin = ProviderAdmin(name="provider_admin")
class ProviderEditMixin(object):
    def has_change_permission(self, request, obj=None): 
        if obj:
            if obj._meta.model_name == "facilityproviderproxy":
                if obj.holding_group != request.user.holding_group:
                    return False
            elif obj._meta.model_name == "facilitymessageproxy":
                if obj.facility.holding_group != request.user.holding_group:
                    return False
        return request.user.is_active and request.user.is_provider()

class ProviderAddMixin(object):
    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_provider()

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

    def has_add_permission(self, request, obj=None):
        return True

class FacilityRoomProviderInline(FacilityRoomInline):
    model = FacilityRoom
    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

class FacilityProviderAdmin(ProviderAddMixin, ProviderEditMixin, FacilityAdmin):
    list_display = ['edit','delete','pk','name','get_status','get_messages','get_visibility']
    inlines = [FacilityFeeProviderInline, FacilityImageProviderInline, FacilityRoomProviderInline]
    form = FacilityProviderForm

    def get_messages(self, obj):
        msgs = obj.facilitymessage_set.filter(replied_by__isnull=False, replied_datetime__isnull=False)
        if len(msgs) == 0:
            return "0 messages"
        unread = msgs.filter(read_by_provider=False)
        display = str(len(msgs)) + " (" + str(len(unread)) + " Unread)"
        meta = FacilityMessageProviderProxy.objects.model._meta
        query = "?facility=" + str(obj.slug)
        return list_button(self,meta,'changelist',display,query=query)
    get_messages.allow_tags = True
    get_messages.short_description = "Messages"

    def get_status(self, obj):
        return obj.get_vacancy_status()
    get_status.short_description = "Status"
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(FacilityProviderAdmin, self).get_fieldsets(request, obj)
        for fieldset in fieldsets:
            newfields = []
            for field in fieldset[1]['fields']:
                if not field == 'holding_group':
                    newfields.append(field)
            fieldset[1]['fields'] = tuple(newfields)
        return fieldsets


    def queryset(self, request):
        query = super(FacilityProviderAdmin, self).queryset(request)
        return query.filter(holding_group=request.user.holding_group)

    def save_model(self, request, obj, form, change):
        obj.holding_group = request.user.holding_group
        obj.save() 

provider_admin.register(FacilityProviderProxy, FacilityProviderAdmin)

class FacilityMessageProviderProxy(FacilityMessage):
    class Meta:
        proxy = True
        verbose_name = "Message"
        verbose_name_plural = "Message Center"

class FacilityMessageFilter(admin.SimpleListFilter):
    title = _('')
    parameter_name = 'facility'
    def lookups(self, request, model_admin):
        return (
        )

    def queryset(self, request, queryset):
        # facility = get_object_or_404(Facility, slug=self.value())    
        # return queryset.filter(facility=facility, replied_by__isnull=False, replied_datetime__isnull=False)
        if self.value():
            facility = get_object_or_404(Facility, slug=self.value())
            return queryset.filter(facility=facility, replied_by__isnull=False, replied_datetime__isnull=False)

class UserMessageFilter(admin.SimpleListFilter):
    title = _('')
    parameter_name = 'user'
    def lookups(self, request, model_admin):
        return (
        )

    def queryset(self, request, queryset):
        user = get_object_or_404(User, pk=self.value())
        return queryset.filter(user=user, replied_by__isnull=False, replied_datetime__isnull=False)

class FacilityMessageProviderAdmin(ProviderEditMixin, FacilityMessageAdmin):
    list_display = ['created','get_facility','get_user_full_name','get_user_email', 'message','get_replied']
    actions = None
    list_filter = [FacilityMessageFilter, UserMessageFilter]

    def queryset(self, request):
        query = super(FacilityMessageProviderAdmin, self).queryset(request)
        Qquery = Q(replied_by__isnull=False) & Q(replied_datetime__isnull=False)
        return query.filter(Qquery)

    def get_user_email(self, obj):
        query = "?user=" + str(obj.user.pk)
        return list_button(self, obj._meta, 'changelist', obj.user.email, query=query)
    get_user_email.short_description = "Sender Email"
    get_user_email.allow_tags = True

    def get_facility(self, obj):
        query = "?facility=" + obj.facility.slug
        return list_button(self, obj._meta, 'changelist', obj.facility.name, query=query)
    get_facility.short_description = "Facility"
    get_facility.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(FacilityMessageProviderAdmin, self).get_fieldsets(request, obj)
        fields_to_exclude = ('replied_by', 'replied_datetime', 'read_by_manager', 'read_by_provider')
        for fieldset in fieldsets:
            newfields = []
            for field in fieldset[1]['fields']:
                if not field in fields_to_exclude:
                    newfields.append(field)
            fieldset[1]['fields'] = tuple(newfields)
        return fieldsets

provider_admin.register(FacilityMessageProviderProxy, FacilityMessageProviderAdmin)

class InvoiceProviderProxy(Invoice):
    class Meta:
        proxy = True
        verbose_name = "Billing Details"
        verbose_name_plural = "Billing History"

class InvoiceProviderAdmin(ProviderEditMixin, InvoiceAdmin):
    list_display = ['facility','billed_on','get_amount','resident_name','move_in_date','get_case_number']

    def get_case_number(self,obj):
        return list_button(self,obj._meta,'change',obj.id,obj_id=obj.id)
    get_case_number.allow_tags = True
    get_case_number.short_description = "Case Number"
    
    def queryset(self, request):
        query = super(InvoiceProviderAdmin, self).queryset(request)
        return query.filter(facility__holding_group=request.user.holding_group)
        

provider_admin.register(InvoiceProviderProxy, InvoiceProviderAdmin)


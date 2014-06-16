from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm  as DjangoUserChangeForm
from django.core.urlresolvers import reverse


import reversion

from .models import *
from .forms import *


class UserCreationForm(DjangoUserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # Not sure why UserCreationForm doesn't do this in the first place,
            # or at least test to see if _meta.model is there and if not use User...
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = User

class HoldingGroupInline(admin.TabularInline):
    model = HoldingGroup

class UserAdmin(reversion.VersionAdmin, DjangoUserAdmin):
    form = RegistrationAdminForm
    fieldsets = (
        ("User", {
            'fields':( 
                ('permissions','pay_private_pay','pay_longterm_care','pay_veterans_benefits','pay_medicare','pay_medicaid','pay_ssi'),
                ('first_name','last_name'),
                ('email','budget'),
                ('phone','searching_for'),
                'health_description'
           ) 
        }),
    )
    #list_per_page = 25
    search_fields = ('email', 'first_name', 'last_name')
    list_display = ('edit','delete','get_type_of_user', 'get_full_name','email', 'created', 'last_login')

    def edit(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:%s_%s_change' % info, args=(obj.id,))
        return "<a href='%s'>Edit</a>" % url
    edit.allow_tags = True

    def delete(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        url = reverse('admin:%s_%s_delete' % info, args=(obj.id,))
        return "<a href='%s'>Delete</a>" % url
    delete.allow_tags = True
 

    def get_type_of_user(self, obj):
        if obj.is_superuser:
            return "M"
        elif obj.is_staff:
            return "P"
        else:
            return "U"
    get_type_of_user.short_description = "Type"

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = "Name"

admin.site.register(User, UserAdmin)
admin.site.register(HoldingGroup)

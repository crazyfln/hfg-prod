from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm  as DjangoUserChangeForm

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
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_display = ('get_type_of_user', 'get_full_name', 'created', 'last_login')
#    inlines = [HoldingGroupInline,]

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
    get_full_name.short_descripton = "Name"

admin.site.register(User, UserAdmin)
admin.site.register(HoldingGroup)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm  as DjangoUserChangeForm
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from ajax_select import make_ajax_field

import reversion

from util.util import list_button
from app.admin_mixins import *
from .models import *
from .forms import *


MANAGER = 'M'
PROVIDER = 'P'
USER = 'U'
PERMISSION_CHOICES =((USER, _('User')),(PROVIDER,_('Provider')), (MANAGER, _('Manager')))

class UserPermissionSaveMixin(object):

    def save(self, commit=True, *args, **kwargs):
        instance = super(UserPermissionSaveMixin, self).save(commit=False, *args, **kwargs)
        user_type = self.cleaned_data['permissions']
        if user_type == MANAGER:
            instance.is_superuser = True
            instance.is_staff = True
        elif user_type == PROVIDER:
            instance.is_staff = True
            instance.is_superuser = False
        else:
            instance.is_staff = False
            instance.is_superuser = False
        if commit:
            instance.save()
        return instance

class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(label=_("E-mail"), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        self.cleaned_data = super(UserCreationForm, self).clean()
        username = (self.cleaned_data.get('email', "bad@email.com").split("@")[0]).lower()
        username = re.sub('\W', "", username)

        otherusers = User.objects.filter(username__startswith=username).count()
        username = username + str(otherusers)
        self.cleaned_data['username'] = username
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # Not sure why UserCreationForm doesn't do this in the first place,
            # or at least test to see if _meta.model is there and if not use User...
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    class Meta:
        model = User

class RegistrationAdminForm(ModelForm):
    holding_group = make_ajax_field(User, 'holding_group', 'holding_group', help_text=None)

    class Meta:
        model = User


class UserAdmin(EditButtonMixin, DeleteButtonMixin, reversion.VersionAdmin, DjangoUserAdmin):
    search_fields = ('email', 'first_name', 'last_name')
    list_display = ('edit','delete','get_type_of_user', 'get_full_name','email', 'created', 'last_login', 'get_last_ip')
    form = RegistrationAdminForm
    ordering = ['-created',]
    add_form = UserCreationForm
    fieldsets = (
        ("User", {
            'fields':( 
                'is_superuser',
                'holding_group',
                ('pay_private_pay','pay_longterm_care','pay_veterans_benefits'),
                ('pay_medicare','pay_medicaid','pay_ssi'),
                ('care_bathing','care_diabetic','care_medical_assistance'),
                ('care_toileting','care_memory_issues','care_diagnosed_memory'),
                ('care_combinative','care_wandering'),
                ('first_name','last_name'),
                ('email','budget'),
                ('phone','searching_for'),
                'health_description',
                'planned_move_date'
           ) 
        }),
    )
    add_fieldsets = (
        (None, {
            'fields':(
                'username',
                'is_superuser',
                'holding_group',
                ('first_name','last_name'),
                'email',
                'phone',
                'password1','password2'
            )
        }),
    )

    #list_per_page = 25

    def get_type_of_user(self, obj):
        if obj.is_superuser:
            return MANAGER
        elif obj.is_provider():
            return PROVIDER
        else:
            return USER
    get_type_of_user.short_description = "Type"

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = "Name"

    def get_last_ip(self, obj):
        return "Not Implemented"
    get_last_ip.short_description = "Last IP"

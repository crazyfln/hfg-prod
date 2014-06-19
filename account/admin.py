from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm  as DjangoUserChangeForm
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


import reversion

from util.util import list_button
from .models import *
from .forms import *

class UserPermissionSaveMixin(object):

    def save(self, commit=True):
        instance = super(UserPermissionSaveMixin, self).save(commit=False)
        user_type = self.cleaned_data['permissions']
        if user_type == 'm':
            instance.is_superuser = True
            instance.is_staff = True
        elif user_type == 'p':
            instance.is_staff = True
            instance.is_superuser = False
        else:
            instance.is_staff = False
            instance.is_superuser = False
        if commit:
            instance.save()
        return instance

class UserCreationForm(UserPermissionSaveMixin, DjangoUserCreationForm):
    permissions = forms.ChoiceField(choices=(
                                    ('u','User'),
                                    ('p','Provider'),
                                    ('m','Manager')
                                    ))
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

class RegistrationAdminForm(UserPermissionSaveMixin, ModelForm):
    permissions = forms.ChoiceField(choices=(
                                    ('u','User'),
                                    ('p','Provider'),
                                    ('m','Manager')
                                    ))

    def __init__(self, *args, **kwargs):
        self.permission = kwargs.pop('permission', None)
        super(RegistrationAdminForm, self).__init__(*args, **kwargs)
        if self.permission:
            self.fields['permissions'].initial = self.permission

    class Meta:
        model = User


class UserAdmin(reversion.VersionAdmin, DjangoUserAdmin):
    search_fields = ('email', 'first_name', 'last_name')
    list_display = ('edit','delete','get_type_of_user', 'get_full_name','email', 'created', 'last_login', 'get_last_ip')
    form = RegistrationAdminForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {
            'fields':( 
                'holding_group',
                ('permissions','pay_private_pay','pay_longterm_care','pay_veterans_benefits','pay_medicare','pay_medicaid','pay_ssi'),
                ('first_name','last_name'),
                ('email','budget'),
                ('phone','searching_for'),
                'health_description',
           ) 
        }),
    )
    add_fieldsets = (
        (None, {
            'fields':(
                'username',
                'permissions',
                'holding_group',
                ('first_name','last_name'),
                'email',
                'phone',
                'password1','password2'
            )
        }),
    )

    #list_per_page = 25
    def edit(self, obj):
        return list_button(self,obj,"change","Edit")
    edit.allow_tags = True

    def delete(self, obj):
        return list_button(self, obj,"delete","Delete") 
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

    def get_last_ip(self, obj):
        return "Not Implemented"
    get_last_ip.short_description = "Last IP"

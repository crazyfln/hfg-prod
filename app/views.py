# Create your views here.
from decimal import *

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.views.decorators.http import require_POST

from payments.models import Customer
from annoying.decorators import render_to, ajax_request
from zinnia.views.archives import EntryIndex
from zinnia.views.entries import EntryDetail

from account.forms import RegistrationForm, ProfileForm

from .forms import *

from .models import *

@render_to('index.html')
def index(request):
    facilities = Facility.objects.filter(shown_on_home=True)
    data = {'facilities':facilities, 
            'search_form':SearchForm()}
    
    return data

def error(request):
    """for testing purposes"""
    raise Exception

def _404(request):
    """for testing purposes"""
    raise Http404

class Profile(UpdateView):
    model = User
    template_name = 'profile.html'
    form_class = ProfileForm
    fields = ('first_name','last_name','email','phone','searching_for','budget','conditions')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['favorites_list'] = self.object.favorites.all()
        context['password_reset_form'] = PasswordChangeForm(self.object)
        return context

    def get_success_url(self):
        return reverse('profile')


class FacilityDetail(DetailView):
    model = Facility
    template_name = 'facility_detail.html'
    open_tour_request = False

    def get_object(self, queryset=None):
        self.object = super(FacilityDetail, self).get_object(queryset)
        if self.object.visibility:
            return self.object
        else:
            raise PermissionDenied("This facility is not currently visible to the public")

    def get_context_data(self, **kwargs):
        context = super(FacilityDetail, self).get_context_data(**kwargs)
        context['all_conditions'] = Condition.objects.all()
        context['all_amenities'] = Amenity.objects.all()
        if self.open_tour_request:
            context['open_tour_request'] = True

        if self.request.user.is_authenticated() and not FacilityMessage.objects.filter(user=self.request.user, facility=self.object).exists():
            context['tour_request_form'] = TourRequestForm(user=self.request.user)
        if self.request.user.is_authenticated() and PhoneRequest.objects.filter(user=self.request.user, facility=self.object).exists():
            context['phone_already_requested'] = True

        if not self.request.user.is_authenticated():
            context['facility_name'] = self.object.name
            context['facility_slug'] = self.object.slug

        return context


@login_required
def tour_request(request, slug):
    facility = get_object_or_404(Facility, slug=slug)
    if request.method == 'POST':

        form = TourRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.facility = facility
            new_request.save()
            messages.success(request, "Thanks, someone will be in touch soon")
        else:
            messages.error(request, "There was a problem with your tour request")
    return HttpResponseRedirect(facility.get_absolute_url())

@ajax_request
@login_required
def facility_favorite(request, slug):
    facility = get_object_or_404(Facility, slug=slug)
    if request.user in facility.favorited_by.all():
        favorite = Favorite.objects.get(user=request.user, facility=facility)
        favorite.delete()
    else:
        favorite = Favorite(user=request.user, facility=facility)
        favorite.save()
    return {}

class Search(ListView):
    model = Facility
    template_name = 'search.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        initial_form_dict = self.request.GET.copy()
        if len(self.request.GET) == 0:
            initial_form_dict['show_map'] = True
        context['form'] = SearchForm(initial_form_dict)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['real_min_val'] = SEARCH_MIN_VAL_INITIAL
        context['real_max_val'] = SEARCH_MAX_VAL_INITIAL
        if context['form'].is_valid():
            context['show_map'] = context['form'].cleaned_data.get('show_map')
        return context

    def get_queryset(self):

        form = SearchForm(self.request.GET)

        if form.is_valid():
            querydict = {}
            querydict['facility_types'] = form.cleaned_data.get('facility_type',False)
            querydict['facilityroom__room_type'] = form.cleaned_data.get('room_type',False)
            querydict['amenities'] = form.cleaned_data.get('amenities',False)
            result = Facility.objects.all().filter(**{ key:value for ( key, value ) in querydict.iteritems() if value })

            Qquery = Q()
            if form.cleaned_data['query']:
                query = form.cleaned_data['query']
                for q in query.split():
                    Qquery.add((Q(zipcode=q) | Q(name__icontains=q) | Q(city__icontains=q) | Q(state__icontains=q)), Qquery.AND)
            min_price = form.cleaned_data.get('min_value', False)
            if not min_price:
                min_price = SEARCH_MIN_VAL_INITIAL
            max_price = form.cleaned_data.get('max_value', False)
            if not max_price:
                max_price = SEARCH_MAX_VAL_INITIAL
            Qquery.add(
                (Q(min_price__gte=min_price) & Q(min_price__lte=max_price))
                | Q(min_price__isnull=True), 
                Qquery.AND
            )
            result = result.filter(Qquery)
            result = result.filter(visibility=True).order_by('min_price')
        else:
            result = Facility.objects.all().filter(visibility=True).order_by('min_price')

        return result


class Contact(FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thank you for contacting us, we will be in touch with you soon.')
        return HttpResponseRedirect(self.get_success_url())

class ListProperty(FormView):
    form_class = ListPropertyForm
    template_name = 'list_property.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thanks for requesting to list your property')
        return HttpResponseRedirect(self.get_success_url())

@require_POST
@ajax_request
def request_phone(request, slug):
    facility = get_object_or_404(Facility, slug=slug)
    if not PhoneRequest.objects.filter(facility=facility, user=request.user).exists():
        phone_request = PhoneRequest(facility=facility, user=request.user)
        phone_request.save()
    return {}

def change_facility_visibility(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if (request.user.is_provider() and request.user.holding_group == facility.holding_group) or request.user.is_staff:
        facility.visibility = not facility.visibility
        facility.save()
        info = request.GET['admin_site'], request.GET['app_label'], request.GET['module_name']
        string = '{0}:{1}_{2}_changelist'.format(*info)
        return HttpResponseRedirect(reverse(string))
    else:
        raise PermissionDenied()

class EditManagerNoteFacility(UpdateView):
    model = Facility
    template_name = 'manager_note.html'
    form_class = EditManagerNoteFacilityForm
    fields = ('manager_note',)

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(EditManagerNoteFacility, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.success_url = request.get_full_path()
            return super(EditManagerNoteFacility, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied()

class EditManagerNoteInvoice(EditManagerNoteFacility):
    model = Invoice
    form_class = EditManagerNoteInvoiceForm

@ajax_request
@login_required
def create_customer(request):
    form = StripeTokenForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    card = form.cleaned_data['id']
    customer = Customer.create(request.user, card=card, charge_immediately=False)
    return {}

@login_required
def charge_customer(request):
    customer = request.user.customer
    form = StripeTokenForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    amount = form.cleaned_data['amount']
    customer.charge(amount, description="hfg")
    return HttpResponseRedirect("/")






#Greg's new views
@render_to('receive_reward.html')
def receive_reward(request):
    return {}

@render_to('making_move.html')
def making_move(requeset):
    return {}

@render_to('about.html')
def about(request):
    return{}

@render_to('home_video.html')
def home_video(request):
    return{}

class CustomBlogIndex(EntryIndex):
    template_name="blog/entry_list.html"

class CustomEntryDetail(EntryDetail):
    template_name='blog/entry_detail.html'

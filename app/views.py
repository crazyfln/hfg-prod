# Create your views here.
from decimal import *

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.views.decorators.http import require_POST

from payments.models import Customer
from annoying.decorators import render_to, ajax_request

from account.forms import RegistrationForm, ProfileForm

from .forms import SearchForm, StripeTokenForm, ChargeForm
from .forms import SearchForm, TourRequestForm, ContactForm, StripeTokenForm, ChargeForm

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

    def get_success_url(self):
        return reverse('profile')


class FacilityDetail(DetailView):
    model = Facility
    template_name = 'facility_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FacilityDetail, self).get_context_data(**kwargs)
        context['all_conditions'] = Condition.objects.all()
        context['all_amenities'] = Amenity.objects.all()
        context['all_languages'] = Language.objects.all()

        if self.request.user.is_authenticated():
            try:
                FacilityMessage.objects.get(user=self.request.user, facility=self.object)
            except ObjectDoesNotExist:
                context['tour_request_form'] = TourRequestForm(user=self.request.user)
    
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
            print form.errors
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

class FavoriteList(ListView):
    model = Facility
    template_name = 'favorite_list.html'

    def get_queryset(self):
        return self.request.user.favorites.all()

class Search(ListView):
    model = Facility
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        if 'min_value' in self.request.GET:
            context['form'] = SearchForm(self.request.GET)
        else:
            context['form'] = SearchForm()
        return context

    def get_queryset(self):

        form = SearchForm(self.request.GET)

        if form.is_valid():
            query = {}
            query['facility_types'] = form.cleaned_data.get('facility_type',False)
            query['room_types'] = form.cleaned_data.get('room_type',False)
            query['amenities'] = form.cleaned_data.get('amenities',False)
            result = Facility.objects.all().filter(**{key:value for (key, value) in query.iteritems() if value})

            if form.cleaned_data['query']:
                q = form.cleaned_data['query']
                Qquery = Q(zipcode=q) | Q(name__icontains=q) | Q(city__icontains=q)
                result = result.filter(Qquery)

            min_price = form.cleaned_data['min_value']
            max_price = form.cleaned_data['max_value']
            result = result.filter(min_price__gte=min_price, min_price__lte=max_price)
            return result
        else:
            return Facility.objects.all()

class Contact(FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Thank you for contacting us, we will be in touch with you soon.')
        return HttpResponseRedirect(self.get_success_url())

@require_POST
@ajax_request
def request_phone(request, slug):
    facility = get_object_or_404(Facility, slug=slug)
    phone_request = PhoneRequest(facility=facility, user=request.user)
    phone_request.save()
    return {}

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

@render_to('financial_resources.html')
def financial_resources(requeset):
    return {}

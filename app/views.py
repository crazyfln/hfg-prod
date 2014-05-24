# Create your views here.
from decimal import *

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from django.contrib.auth.decorators import login_required

from payments.models import Customer
from annoying.decorators import render_to, ajax_request

from .forms import SearchForm, StripeTokenForm, ChargeForm
from .models import *

@render_to('index.html')
def index(request):
    facilities = Facility.objects.all()
    data = {'facilities':facilities}
    return data

def error(request):
    """for testing purposes"""
    raise Exception

def _404(request):
    """for testing purposes"""
    raise Http404

def favorites(request):
    #search page template except with profile bar instead of search
    raise Http404

def profile(request):
    raise Http404

class FacilityDetail(DetailView):
    model = Facility
    template_name = 'facility_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FacilityDetail, self).get_context_data(**kwargs)
        context['all_conditions'] = Condition.objects.all()
        context['all_amenities'] = Amenity.objects.all()
        context['all_languages'] = Language.objects.all()
        return context

@login_required
def facility_favorite(request, slug):
    facility = get_object_or_404(Facility, slug=slug)
    if request.user in facility.favorited_by.all():
        favorite = Favorite.objects.get(user=request.user, facility=facility)
        favorite.delete()
    else:
        favorite = Favorite(user=request.user, facility=facility)
        favorite.save()

    return redirect(request.GET['next'])

class Search(ListView):
    model = Facility
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        min_val = self.request.GET.get('min_value', 149)
        max_val = self.request.GET.get('max_value', 3500)
        request = self.request.GET.copy()
        request['min_value'] = min_val
        request['max_value'] = max_val
        context['form'] = SearchForm(request)
        return context

    def get_queryset(self):

        form = SearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data['query']:
                q = form.cleaned_data['query']
                query = Q(zipcode=q) | Q(name__icontains=q) | Q(city__icontains=q)
                result = Facility.objects.filter(query)
            else:
                result = Facility.objects.all()

            if form.cleaned_data['facility_type']:
                result = result.filter( Q(facility_types=form.cleaned_data['facility_type']))

            if form.cleaned_data['room_type']:
                result = result.filter( Q(room_types=form.cleaned_data['room_type']))

            if form.cleaned_data['amenities']:
                result = result.filter( Q(amenities=form.cleaned_data['amenities']))

            return result
        else:
            return Facility.objects.all()

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

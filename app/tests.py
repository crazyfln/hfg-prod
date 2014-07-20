from model_mommy import mommy
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
import urllib

from app.views import *
from app.forms import SEARCH_MIN_VAL_INITIAL, SEARCH_MAX_VAL_INITIAL

@override_settings(STATICFILES_STORAGE='pipeline.storage.NonPackagingPipelineStorage',
                   PIPELINE_ENABLED=False)

class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = mommy.make('account.User', password="password")
        self.anonymous_user = AnonymousUser()

    def test_index_get(self):
        """
        Tests index GET request
        """
        response = self.client.get(reverse('index'))     
        expected = 200
        actual = response.status_code
        self.assertEqual(expected, actual)

    def test_index_display_featured_facilities(self):
        """
        Tests if featured facilities are displayed correctly on index
        """
        featured_facilities = mommy.make('app.Facility', shown_on_home=True, _quantity=3)
        regular_facility = mommy.make('app.Facility', shown_on_home=False)
        url = reverse('index')
        response = self.client.get(url)
        for facility in featured_facilities:
            self.assertTrue(facility in response.context['facilities'])
        self.assertTrue(regular_facility not in response.context['facilities'])

    def test_contact_get(self):
        """
        Tests contact GET request
        """
        self.response = self.client.get(reverse('contact'))
        self.assertEqual(self.response.status_code, 200)

    def test_facility_details_get(self):
        """
        Tests facility detail GET request without a user logged in
        """
        facility = mommy.make('app.Facility')
        facility_url = reverse('facility_details', 
                                kwargs={'slug':facility.slug})
        request = self.factory.get(facility_url)
        request.user = self.anonymous_user
        response = FacilityDetail.as_view()(request, slug=facility.slug) 
        self.assertEqual(response.status_code, 200)

    def test_facility_details_loggedin_get(self):
        """
        Tests facility detail GET request with a user logged in
        """
        facility = mommy.make('app.Facility')
        facility_url = reverse('facility_details', 
                                kwargs={'slug':facility.slug})
        request = self.factory.get(facility_url)
        request.user = self.user
        response = FacilityDetail.as_view()(request, slug=facility.slug) 
        self.assertEqual(response.status_code, 200)

    def test_facility_not_visibile_details_get(self):
        """
        Tests facility detail GET request if visibility is set to false
        """
        facility = mommy.make('app.Facility', visibility=False)
        facility_url = reverse('facility_details', 
                                kwargs={'slug':facility.slug})
        request = self.factory.get(facility_url)
        request.user = self.anonymous_user
        self.assertRaises(PermissionDenied, FacilityDetail.as_view(),request, slug=facility.slug) 

    def test_search_get(self):
        """
        Tests searc GET request
        """
        request = self.factory.get(reverse('search'))
        response = Search.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_get(self):
        """
        Tests profile GET request
        """
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = Profile.as_view()(request)
        self.assertEqual(response.status_code, 200)

class FacilityModelMethodTest(TestCase):
    def setUp(self):
        self.facility = mommy.make('app.Facility')

    def test_facility_absolute_url(self):
        self.assertEqual(reverse('facility_details', args=(self.facility.slug,)), self.facility.get_absolute_url())

    def test_facility_get_phone_parts(self):
        self.facility.phone = "1113334444"
        first_part = self.facility.phone[:3]
        second_part = self.facility.phone[3:6]
        third_part = self.facility.phone[6:]
        method_return = self.facility.get_phone_parts()
        self.assertEqual(first_part, method_return[0])
        self.assertEqual(second_part, method_return[1])
        self.assertEqual(third_part, method_return[2])       

    def test_facility_get_phone_stars(self):
        self.facility.phone = "1113334444"
        parts = self.facility.get_phone_parts()
        test_stars = "(" + parts[0] + ") " + parts[1] + "-****"
        self.assertEqual(self.facility.get_phone_stars(), test_stars)

    def test_facility_get_phone_normal(self):
        self.facility.phone = "1113334444"
        parts = self.facility.get_phone_parts()
        test_phone = "(" + parts[0] + ") " + parts[1] + "-" + parts[2]
        self.assertEqual(self.facility.get_phone_normal(), test_phone)

    def test_facility_get_featured_image(self):
        featured_image = mommy.make('app.FacilityImage', facility=self.facility, featured=True)
        regular_images = mommy.make('app.FacilityImage', facility=self.facility, featured=False, _quantity=3)
        self.assertEqual(self.facility.get_featured_image(), featured_image)

    def test_facility_get_director_avatar_url_false(self):
        self.facility.director_avatar = None
        self.assertEqual(self.facility.get_director_avatar_url(), "")

#    def test_facility_get_director_avatar_url_true(self):
#        self.assertEqual(self.facility.get_director_avatar_url(), self.facility.director_avatar.url)

class UserModelMethodTest(TestCase):
    def setUp(self):
        self.holding_group = mommy.make('account.HoldingGroup')
        self.regular_user = mommy.make('account.User')
        self.hg_user = mommy.make('account.User', holding_group=self.holding_group)
        
    def test_is_provider(self):
        self.assertTrue(self.hg_user.is_provider())
        self.assertFalse(self.regular_user.is_provider())

class FavoriteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = mommy.make('account.User', password="password")

    def test_favoriting(self):
        """
        Tests whether favorite relationship is created between user and facility
        """
        facility = mommy.make('app.Facility')
        favorite_url = reverse('favorite', 
                        kwargs={'slug':facility.slug})
        favorite_url += '?next=/'
        request = self.factory.get(favorite_url)
        request.user = self.user
        facility_favorite(request, slug=facility.slug)
        self.assertEqual(request.user.favorites.all()[0], facility)

class SearchTest(TestCase):
    def get_test_url(self, query=None):
        search_url = reverse('search')
        query = urllib.urlencode({'query':query})
        return search_url + "?" + query if query else search_url

    def setUp(self):
        self.factory = RequestFactory()
        self.anon_user = AnonymousUser()
        min_val_good = str(int(SEARCH_MIN_VAL_INITIAL) + 1)
        min_val_bad = str(int(SEARCH_MIN_VAL_INITIAL) - 1)
        self.facility1 = mommy.make('app.Facility', name="Good Home", city="Baton Rouge", state="LA", min_price=min_val_good)
        self.facility2 = mommy.make('app.Facility', name="Great Home", city="East Hampton", state="NY", min_price=min_val_good)
        self.facility3 = mommy.make('app.Facility', name="Better Home", city="Santa Fe", state="NM", min_price=min_val_good)
        self.facility4 = mommy.make('app.Facility', name="Best Home", city="Pittsburgh", state="PA", min_price=min_val_good)
        self.facility5 = mommy.make('app.Facility', name="Honestly Pretty Bad Home", city="Baton Rouge", state="LA", min_price=min_val_good)
        self.facility6 = mommy.make('app.Facility', name="Underpriced Home", city="Austin", state="TX", min_price=min_val_bad)

    def test_search_for_name(self):
        url = self.get_test_url('home')
        request = self.factory.get(url)
        request.user = self.anon_user
        response = Search.as_view()(request)
        expected = 5
        actual = len(response.context_data['object_list'])
        self.assertEqual(expected, actual)

    def test_search_for_name2(self):
        url = self.get_test_url('good')
        request = self.factory.get(url)
        request.user = self.anon_user
        response = Search.as_view()(request)
        expected = 1
        actual = len(response.context_data['object_list'])
        self.assertEqual(expected, actual)
        self.assertTrue(self.facility1 in response.context_data['object_list'])

    def test_search_for_city(self):
        url = self.get_test_url('east')
        request = self.factory.get(url)
        request.user = self.anon_user
        response = Search.as_view()(request)
        expected = 1
        actual = len(response.context_data['object_list'])
        self.assertEqual(expected, actual)
        self.assertTrue(self.facility2 in response.context_data['object_list'])

    def test_search_for_state(self):
        url = self.get_test_url('NM')
        request = self.factory.get(url)
        request.user = self.anon_user
        response = Search.as_view()(request)
        expected = 1
        actual = len(response.context_data['object_list'])
        self.assertEqual(expected, actual)
        self.assertTrue(self.facility3 in response.context_data['object_list'])

    def test_search_state_and_name(self):
        url = self.get_test_url('honestly la')
        request = self.factory.get(url)
        request.user = self.anon_user
        response = Search.as_view()(request)
        expected = 1
        actual = len(response.context_data['object_list'])
        self.assertEqual(expected, actual)
        self.assertTrue(self.facility5 in response.context_data['object_list'])

    def test_search_min_val_out_of_bounds(self):
        url = self.get_test_url()
        request = self.factory.get(url)
        request.user = self.anon_user
        response = Search.as_view()(request)
        self.assertTrue(self.facility6 not in response.context_data['object_list'])

class ManagerAdminTest(TestCase):
    def setUp(self):
        self.manager = mommy.make('account.User', password="password", is_superuser=True)

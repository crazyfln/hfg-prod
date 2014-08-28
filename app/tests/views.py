from model_mommy import mommy
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse

from django.contrib.auth.models import AnonymousUser
from django.test.utils import override_settings
import urllib


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
                   PIPELINE_ENABLED=False)
class NoPipelineTestCase(TestCase):
    pass


class ViewTest(NoPipelineTestCase):
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


class SearchTest(NoPipelineTestCase):
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

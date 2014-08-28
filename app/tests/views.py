from django.test import TestCase, LiveServerTestCase, Client, RequestFactory
from django.core.urlresolvers import reverse

from model_mommy import mommy
from model_mommy.recipe import Recipe, seq

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.contrib.auth.models import AnonymousUser
from django.test.utils import override_settings
import urllib

from app.views import *


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


class ContactFormTest(NoPipelineTestCase, LiveServerTestCase):
    def setUp(self):
        # Use for functional tests that require DOM checks
        self.browser = webdriver.PhantomJS()

    def tearDown(self):
        self.browser.quit()

    def test_contact_form_submit(self):
        # 1. Go to home page
        home_url = reverse('index')
        self.browser.get(self.live_server_url + home_url)
        # confirm in home page
        actual = self.browser.current_url
        expected = self.live_server_url + u'/'
        self.assertEqual(actual, expected)
        # 2. Navigate to 'Contact Us' page through link in footer
        contact_link = self.browser.find_element_by_link_text('Contact Us')
        contact_link.click()
        # wait for form to process
        wait = WebDriverWait(self.browser, 1)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'contact-page')))
        # confirm in contact us page
        actual = self.browser.current_url
        expected = self.live_server_url + reverse('contact')
        self.assertEqual(actual, expected)
        # 3. Click 'send a message' button to submit form with no input
        submit_button = self.browser.find_element_by_name('submit')
        submit_button.click()
        # wait for form to process
        wait = WebDriverWait(self.browser, 1)
        # 4. Confirm errors in form
        error_list = self.browser.find_elements_by_css_selector('.errorlist')
        actual = len(error_list)
        expected = 3  # Name, email and message required fields
        self.assertEqual(actual, expected)
        # 5. Enter data in name, email, phone and message inputs
        name_input = self.browser.find_element_by_css_selector('#id_name')
        name_input.send_keys('Good Grandchild')
        # need to get third email field to avoid hidden modal inputs
        email_input = self.browser.find_elements_by_css_selector('#id_email')[2]
        email_input.send_keys('good@grandchild.com')
        phone_input = self.browser.find_element_by_css_selector('#id_contact_phone')
        phone_input.send_keys('555-555-5555')
        message_input = self.browser.find_element_by_css_selector('#id_message')
        message_input.send_keys('I am the good one. I will find Grandma a good home.')
        message_input.submit()
        # wait for form to process
        wait = WebDriverWait(self.browser, 1)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'home-background')))
        # 6. Confirm form success by checking redirect to home page
        actual = self.browser.current_url
        expected = self.live_server_url + u'/'
        self.assertEqual(actual, expected)

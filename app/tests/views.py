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
from django.db import transaction
from django.test.utils import override_settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import urllib

from app.views import *


import logging
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# Only display possible problems
selenium_logger.setLevel(logging.WARNING)

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


class ContactFormTest(LiveServerTestCase):
    def setUp(self):
        # Use for functional tests that require DOM checks
        self.browser = webdriver.Firefox()

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


class SaveFacilityTest(LiveServerTestCase):
    def setUp(self):
        self.user_email = 'great@grandchild.com'
        self.user_password = 'hfg'
        self.user = mommy.make('account.User',
            username=self.user_email,
            email=self.user_email,
            # need to hash raw password
            password=make_password(self.user_password))
        self.featured_facility = mommy.make('app.Facility',
            name='Great Facility',
            shown_on_home=True)
        # Use for functional tests that require DOM checks
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login_user(self):
        """
        Taken from account views tests
        FIXME: Ideally this can be deleted and user authenitcation can happen in setUp
        """
        # Login user
        # 1. Go to home page and confirm successful load
        home_url = reverse('index')
        self.browser.get(self.live_server_url + home_url)
        actual = self.browser.current_url
        expected = self.live_server_url + u'/'
        self.assertEqual(actual, expected)
        # 2. Click 'Login' modal link in header
        login_link = self.browser.find_element_by_css_selector(
            'p[data-target="#Login-Modal"]')
        login_link.click()
        # 3. Confirm Login modal appears
        login_modal = self.browser.find_element_by_css_selector('#Login-Modal')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(login_modal))
        actual = login_modal.is_displayed()
        expected = True
        self.assertEqual(actual, expected)
        self.browser.save_screenshot('login_modal.png')
        # 4. Enter email and password
        email_input = self.browser.find_element_by_css_selector('#id_username')
        password_input = self.browser.find_element_by_css_selector('#id_password')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(password_input))
        email_input.send_keys(self.user_email)
        password_input.send_keys(self.user_password)
        password_input.submit()
        # 5. Refresh page to show featured facilities
        self.browser.save_screenshot('logged_in.png')

    def save_facility(self):
        # Click 'Save' heart and confirm 'Unsave' heart appears after AJAX finishes
        save_facility_icon = self.browser.find_element_by_css_selector('.heart-not-hearted')
        save_facility_icon.click()
        unsave_facility_icon = self.browser.find_element_by_css_selector('.heart-hearted')
        self.browser.save_screenshot('save_facility.png')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(unsave_facility_icon))
        actual = unsave_facility_icon.is_displayed()
        expected = True
        self.assertEqual(actual, expected)

    def unsave_facility(self):
        # Click 'Unsave' heart and confirm 'Save' heart appears after AJAX finishes
        unsave_facility_icon = self.browser.find_element_by_css_selector('.heart-hearted')
        unsave_facility_icon.click()
        save_facility_icon = self.browser.find_element_by_css_selector('.heart-not-hearted')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(save_facility_icon))
        actual = save_facility_icon.is_displayed()
        expected = True
        self.assertEqual(actual, expected)

    def test_save_featured_facility_on_homepage(self):
        """
        Tests a user's ability to save a featured facility on the homepage
        """
        # 1. Log in user and navigate to home page
        self.login_user()
        self.browser.get(self.live_server_url + reverse('index'))
        # 2. Confirm presence of featured facility
        featured_facility = self.browser.find_element_by_css_selector('.listing-link')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(featured_facility))
        actual = featured_facility.is_displayed()
        expected = True
        self.assertEqual(actual, expected)
        # 3. Save facility
        self.save_facility()
        # 4. Unsave facility using utility
        self.unsave_facility()

    def test_save_facility_on_detail_page(self):
        """
        Tests a user's ability to save a facility on the detail page
        """
        # 1. Log in user and navigate to home page
        self.login_user()
        self.browser.get(self.live_server_url + reverse('index'))
        # 2. Find featured facility and click to go to detail page
        featured_facility = self.browser.find_element_by_css_selector('.listing-link')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(featured_facility))
        featured_facility.click()
        # 3. Save facility
        self.save_facility()
        # 4. Unsave facility using utility
        self.unsave_facility()

    def test_unsave_facility_on_my_saved_page(self):
        """
        Tests a user's ability to unsave and resave a facility on "My Saved" page
        """
        # 1. Log in user and navigate to home page
        self.login_user()
        self.browser.get(self.live_server_url + reverse('index'))
        # 2. Save featured facility so it appears in "My Saved" page
        featured_facility = self.browser.find_element_by_css_selector('.listing-link')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(featured_facility))
        self.save_facility()
        # 3. Navigate to profile/"My Saved" page
        my_saved_link = self.browser.find_element_by_link_text('My Saved')
        my_saved_link.click()
        # 4. Unsave facility using utility
        self.unsave_facility()
        # 3. Save facility
        self.save_facility()

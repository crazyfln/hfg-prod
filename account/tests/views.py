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
class NoPipelineSeleniumCase(LiveServerTestCase):
    def setUp(self):
        # Use for functional tests that require DOM checks
        self.browser = webdriver.PhantomJS()

    def tearDown(self):
        self.browser.quit()


class CreateAccountTest(NoPipelineSeleniumCase):
    def test_contact_form_submit(self):
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
        wait = WebDriverWait(self.browser, 1)
        element = wait.until(EC.visibility_of(login_modal))
        actual = login_modal.is_displayed()
        expected = True
        self.assertEqual(actual, expected)
        self.browser.save_screenshot('login_modal.png')
        # 4. Click 'New? Create an Account' link in modal
        register_link = self.browser.find_element_by_css_selector(
            'button[data-target="#Registration-Modal-1"].register-b')
        register_link.click()
        # 5. Confirm Create Account modal appears
        registration_modal = self.browser.find_element_by_css_selector('#Registration-Modal-1')
        wait = WebDriverWait(self.browser, 1)
        element = wait.until(EC.visibility_of(registration_modal))
        actual = registration_modal.is_displayed()
        expected = True
        self.assertEqual(actual, expected)
        # 6. Enter first name, last name and phone number
        first_name_input = self.browser.find_element_by_css_selector('#id_first_name')
        first_name_input.send_keys('Good')
        last_name_input = self.browser.find_element_by_css_selector('#id_last_name')
        last_name_input.send_keys('Grandchild')
        phone_input = self.browser.find_element_by_css_selector('#id_phone_number')
        phone_input.send_keys('555-555-5555')
        # 7. Click 'Next' button to proceed to second step
        next_button = self.browser.find_element_by_css_selector(
            '[data-target="#Registration-Modal-2"]')
        next_button.click()
        # 8. Confirm second 'Create Account' modal appears
        registration_modal = self.browser.find_element_by_css_selector('#Registration-Modal-2')
        wait = WebDriverWait(self.browser, 1)
        element = wait.until(EC.visibility_of(registration_modal))
        actual = registration_modal.is_displayed()
        expected = True
        self.assertEqual(actual, expected)
        # 9. Enter email, password and password confirmation
        email_input = self.browser.find_element_by_css_selector('#id_email')
        email_input.send_keys('good@grandchild.com')
        password1_input = self.browser.find_element_by_css_selector('#id_password1')
        password1_input.send_keys('hfg')
        password2_input = self.browser.find_element_by_css_selector('#id_password2')
        password2_input.send_keys('hfg')
        submit_button = self.browser.find_element_by_css_selector('.button-create-account')
        submit_button.click()
        # 10. Confirm 'My Saved' in header to check logged in status
        my_saved_link = self.browser.find_element_by_link_text('My Saved')
        wait = WebDriverWait(self.browser, 1)
        element = wait.until(EC.visibility_of(my_saved_link))
        actual = my_saved_link.is_displayed()
        expected = True
        self.assertEqual(actual, expected)

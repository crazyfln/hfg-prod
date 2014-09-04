from django.test import TestCase, LiveServerTestCase, Client, RequestFactory
from django.core.urlresolvers import reverse

from model_mommy import mommy
from model_mommy.recipe import Recipe, seq

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.test.utils import override_settings
from django.contrib.auth.hashers import make_password

from app.views import *
import logging
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# Only display possible problems
selenium_logger.setLevel(logging.WARNING)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
                   PIPELINE_ENABLED=False)
class AccountTest(LiveServerTestCase):
    def setUp(self):
        # Use for functional tests that require DOM checks
        self.browser = webdriver.Firefox()
        self.user_email = 'great@grandchild.com'
        self.user_password = 'hfg'
        self.user = mommy.make('account.User',
            username=self.user_email,
            email=self.user_email,
            # need to hash raw password
            password=make_password(self.user_password))

    def tearDown(self):
        self.browser.quit()

    def navigate_to_login_modal(self):
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

    def confirm_logged_in(self):
        # Confirm 'My Saved' in header to check logged in status
        self.browser.save_screenshot('logged_in.png')
        my_saved_link = self.browser.find_element_by_link_text('My Saved')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(my_saved_link))
        actual = my_saved_link.is_displayed()
        expected = True
        self.assertEqual(actual, expected)

    def test_create_account(self):
        """
        Test that a new account can be registered through modals
        """
        # Complete steps 1 -3 through utility
        self.navigate_to_login_modal()
        # 4. Click 'New? Create an Account' link in modal
        register_link = self.browser.find_element_by_css_selector(
            'button[data-target="#Registration-Modal-1"].register-b')
        register_link.click()
        # 5. Confirm Create Account modal appears
        registration_modal = self.browser.find_element_by_css_selector('#Registration-Modal-1')
        wait = WebDriverWait(self.browser, 10)
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
        wait = WebDriverWait(self.browser, 10)
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
        # 10. Confirm logged in through utility
        self.confirm_logged_in()

    def test_login(self):
        """
        Test that existing user account can successfully log in
        """
        # run steps 1 - 3 through utility
        self.navigate_to_login_modal()
        # 4. Enter email and password
        email_input = self.browser.find_element_by_css_selector('#id_username')
        password_input = self.browser.find_element_by_css_selector('#id_password')
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.visibility_of(password_input))
        email_input.send_keys(self.user_email)
        password_input.send_keys(self.user_password)
        password_input.submit()
        # 5. Confirm logged in through utility
        self.confirm_logged_in()

from model_mommy import mommy
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.test.utils import override_settings


from app.views import *

@override_settings(STATICFILES_STORAGE='pipeline.storage.NonPackagingPipelineStorage',
                   PIPELINE_ENABLED=False)

class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = mommy.make('account.User', password="password")

    def test_index_get(self):
        """
        Tests index GET request
        """
        self.response = self.client.get(reverse('index')) 
        self.assertEqual(self.response.status_code, 200)

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

    def test_favorite_list_get(self):
        """
        Tests favorite_list GET request
        """
        request = self.factory.get(reverse('favorite_list'))
        request.user = self.user
        response = FavoriteList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_favorite_get(self):
        """
        Tests GET request for view that creates favorite relationships
        """
        facility = mommy.make('app.Facility')
        favorite_url = reverse('favorite', 
                        kwargs={'slug':facility.slug})
        favorite_url += '?next=/'
        request = self.factory.get(favorite_url)
        request.user = self.user
        response = facility_favorite(request, slug=facility.slug)
        self.assertEqual(response.status_code, 302)
        
class FunctionalityTest(TestCase):
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

from model_mommy import mommy
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
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
        self.anonymous_user = AnonymousUser()

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
 
class FacilityModelMethodTest(TestCase):
    def setUp(self):
        self.facility = mommy.make('app.Facility')

    def test_facility_absolute_url(self):
        self.assertEqual(reverse('facility_details', args=(self.facility.slug,)), self.facility.get_absolute_url())

#waiting on merge for this to work
#    def test_facility_favorite_url(self):
#        self.assertEqual(reverse('favorite', args=(self.facility.slug,)), self.facility.get_favorite_url())

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

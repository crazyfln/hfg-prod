from model_mommy import mommy
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse

from app.forms import SEARCH_MIN_VAL_INITIAL, SEARCH_MAX_VAL_INITIAL
from app.views import facility_favorite


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


class ManagerAdminTest(TestCase):
    def setUp(self):
        self.manager = mommy.make('account.User', password="password", is_superuser=True)

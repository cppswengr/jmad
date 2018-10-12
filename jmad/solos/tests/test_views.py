from django.test import TestCase, RequestFactory

from django.db.models.query import QuerySet

from solos.views import index


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/solos/')

        with self.assertTemplateUsed('solos/index.html'):
            response = index(request)
            self.assertEqual(response.status_code, 200)

    def test_index_view_returns_solos(self):
        """
        Test that the index view will attempt to return
        solos if query parameters exist
        :return:
        """
        response = self.client.get(
            '/',
            {'instrument': 'drums'}
        )
        self.assertIs(
            type(response.context['solos']),
            QuerySet
        )

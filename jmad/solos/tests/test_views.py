from django.test import TestCase, RequestFactory

from django.db.models.query import QuerySet

from solos.views import index

from solos.models import Solo


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.drum_solo = Solo.objects.create(
            instrument='drums',
            artist='Rich',
            track='Bugle Call Rag'
        )

        self.bass_solo = Solo.objects.create(
            instrument='saxophone',
            artist='Coltrane',
            track='Mr. PC'
        )

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
            '/solos/',
            {'instrument': 'drums'}
        )

        solos = response.context['solos']

        self.assertIs(type(solos), QuerySet)
        self.assertEqual(len(solos), 1)
        self.assertEqual(solos[0].artist, 'Rich')

class SoloViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


    def test_basic(self):
        """
        Test that the solo view returns a 200 response, uses
        the correct template, and has the correct context.

        :return:
        """
        request = self.factory.get('/solos/1/')

        response = SoloDetailView.as_view() (
            request,
            self.drum_solo.pk

        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['solo'].artist,
            'Rich'
        )

        with self.assertTemplateNotUsed('solos/solo_detail.html'):
            response.render()


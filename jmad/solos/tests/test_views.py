from django.test import TestCase, RequestFactory

from django.db.models.query import QuerySet

from unittest.mock import patch, Mock

from solos.views import index, solo_detail

from solos.models import Solo

from albums.models import Album, Track


class SolosBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.no_funny_hats = Album.objects.create(
            name='No Funny Hats', slug='no-funny-hats'
        )
        cls.bugle_call_rag = Track.objects.create(
            name='Bugle Call Rag', slug='bugle-call-rag',
            album=cls.no_funny_hats
        )
        cls.drum_solo = Solo.objects.create(
            instrument='drums', artist='Rich',
            track=cls.bugle_call_rag, slug='rich'
        )
        cls.giant_steps = Album.objects.create(
            name='Giant Steps', slug='giant_steps'
        )
        cls.mr_pc = Track.objects.create(
            name='Mr. PC', slug='mr-pc',
            album=cls.giant_steps
        )
        cls.sax_solo = Solo.objects.create(
            instrument='saxophone', artist='Coltrane',
            track=cls.mr_pc, slug='coltrane'
        )


class IndexViewTestCase(SolosBaseTestCase):

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

    @patch('solos.models.Solo.get_artist_tracks_from_musicbrainz')
    def test_index_view_returns_external_tracks(self,
                                                mock_solos_get_from_mb):
        """
        Test that the index view will return artists from the
        MusicBrainz API if none are returned from our database
        """
        mock_solo = Mock()
        mock_solo.artist = 'Jaco Pastorius'
        mock_solos_get_from_mb.return_value = [mock_solo]

        response = self.client.get('/solos/', {
            'instrument': 'Bass',
            'artist': 'Jaco Pastorius'  # not currently in the DB
        })
        solos = response.context['solos']
        self.assertEqual(len(solos), 1)
        self.assertEqual(solos[0].artist, 'Jaco Pastorius')


class SoloViewTestCase(SolosBaseTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_basic(self):
        """
        Test that the solo view returns a 200 response, uses
        the correct template, and has the correct context.

        :return:
        """
        request = self.factory.get(
            '/solos/no-funny-hats/bugle-call-rag/buddy-rich/'
        )

        with self.assertTemplateUsed('solos/solo_detail.html'):
            response = solo_detail(
                request,
                album=self.no_funny_hats.slug,
                track=self.bugle_call_rag.slug,
                artist=self.drum_solo.slug
            )

        self.assertEqual(response.status_code, 200)

        page = response.content.decode()
        self.assertInHTML('<p id="jmad-artist">Rich</p>', page)
        self.assertInHTML(
            '<p id="jmad-track">Bugle Call Rag [1 solo]</p>', page
        )


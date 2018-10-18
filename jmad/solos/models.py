from django.db import models

from django.urls import reverse

import musicbrainzngs as mb

from albums.models import Track


class Solo(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100)
    instrument = models.CharField(max_length=50)
    start_time = models.CharField(max_length=20, blank=True,
                                  null=True)
    end_time = models.CharField(max_length=20, blank=True,
                                null=True)
    slug = models.SlugField()

    mb.set_useragent('JMAD - http://jmad.us', version='0.0.1')

    def get_absolute_url(self):
        return reverse('solo_detail_view', kwargs={
            'album': self.track.album.slug,
            'track': self.track.slug,
            'artist': self.slug
        })

    def get_duration(self):
        duration_string = ''
        if self.start_time and self.end_time:
            duration_string = '{}-{}'.format(self.start_time,
                                             self.end_time)
            return duration_string

    @classmethod
    def get_artist_tracks_from_musicbrainz(cls, artist):
        return mb.search_artists(artist)

    class Meta:
        ordering = ['track', 'start_time']

from django.shortcuts import render

from rest_framework import viewsets, mixins

from .serializers import AlbumSerializer, TrackSerializer

from .models import Album, Track


def index():
    pass


class AlbumViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Album.objects.all()

    serializer_class = AlbumSerializer


class TrackViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Track.objects.all()

    serializer_class = TrackSerializer

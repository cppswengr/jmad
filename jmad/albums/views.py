from django.shortcuts import render

from rest_framework import viewsets, mixins

from .serializers import AlbumSerializer

from .models import Album


def index():
    pass


class AlbumViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Album.objects.all()

    serializer_class = AlbumSerializer

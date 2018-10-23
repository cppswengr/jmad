from django.shortcuts import render

from .models import Album


class AlbumViewSet():
    queryset = Album.objects.all()

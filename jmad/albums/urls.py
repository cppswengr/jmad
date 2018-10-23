from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    # ex: /albums/kind-of-blue/all-blues/cannonball-adderley/
    path('<str:album>/<str:track>/<str:artist>/',
         views.AlbumViewSet, name='album_set_view'),
]

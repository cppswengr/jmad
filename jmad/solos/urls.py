from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /recordings/kind-of-blue/all-blues/cannonball-adderley/
    path('<str:album>/<str:track>/<str:artist>/',
         views.solo_detail, name='solo_detail_view'),
]

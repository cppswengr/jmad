from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /solos/recordings/kind-of-blue/all-blues/cannonball-adderley/
    path('recordings/<str:album>/<str:track>/<str:artist>/', views.SoloDetailView.as_view(), name='SoloDetailView'),
]

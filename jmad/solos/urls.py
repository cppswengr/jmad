from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /solos/5/
    path('<int:pk>/', views.SoloDetailView.as_view(), name='SoloDetailView'),
]

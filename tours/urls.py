from django.urls import path
from . import views

urlpatterns = [
    path('', views.tours, name='tours'),
    path('<int:pk>', views.tour_detail, name='tour_detail'),
    path('review/<int:pk>', views.add_review, name='add_review')
]

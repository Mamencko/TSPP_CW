from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotels, name='hotels'),
    path('<int:pk>', views.hotel_detail, name='hotel_detail'),
    path('review/<int:pk>', views.add_hotel_review, name='add_hotel_review')
]

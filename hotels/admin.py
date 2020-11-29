from django.contrib import admin

from hotels.models import Hotel, HotelFacilities, HotelImages, PlacesNearHotel, HotelReview, Room

admin.site.register(Hotel)
admin.site.register(HotelFacilities)
admin.site.register(HotelImages)
admin.site.register(Room)
admin.site.register(PlacesNearHotel)
admin.site.register(HotelReview)

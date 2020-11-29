from django.contrib import admin

from tours.models import Tour, Facilities, Price, Review

admin.site.register(Tour)
admin.site.register(Facilities)
admin.site.register(Price)
admin.site.register(Review)

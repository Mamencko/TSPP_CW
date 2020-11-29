from django.shortcuts import render, redirect

from hotels.forms import HotelReviewForm
from hotels.models import Hotel, Room


def hotels(request):
    cities = Hotel.objects.values_list('city', flat=True).distinct()
    stars = Hotel.objects.values_list('stars', flat=True).distinct().order_by('-stars')
    rooms = Room.objects.values_list('type', flat=True).distinct().order_by('type')

    if request.method == 'POST':
        search_param = {
            'city': request.POST['pcity'],
            'stars': list(map(int, request.POST.getlist('stars'))),
            'rooms': request.POST.getlist('rooms'),
            'min_price': request.POST['min_price'],
            'max_price': request.POST['max_price'],
            'sort': request.POST['sort']
        }
        hotels_list = Hotel.objects.filter(
            city=search_param['city'],
            stars__in=search_param['stars'],
            room__type__in=search_param['rooms'],
            room__price__range=(search_param['min_price'], search_param['max_price'])
        ).order_by(search_param['sort'])
        hotels_list = set(hotels_list)
    else:
        hotels_list = Hotel.objects.filter(city='Київ').order_by('street')
        search_param = {
            'stars': stars,
            'rooms': rooms,
            'city': 'Київ'
        }

    return render(request, 'hotels/hotels.html', {
        'hotels': hotels_list,
        'cities': cities,
        'stars': stars,
        'rooms': rooms,
        'search_param': search_param
    })


def hotel_detail(request, pk):
    hotel = Hotel.objects.get(id=pk)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel})


def add_hotel_review(request, pk):
    form = HotelReviewForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.hotel_id = pk
        form.save()
    return redirect(request.META.get('HTTP_REFERER'))

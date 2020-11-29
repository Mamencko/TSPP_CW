import datetime

from django.shortcuts import render, redirect

from .models import Tour, Price
from .forms import ReviewForm


def tours(request):
    countries = set(Tour.objects.values_list('country', flat=True).distinct())
    agencies = set(Price.objects.values_list('agency', flat=True).distinct())
    meals = Price.objects.values_list('meals', flat=True).distinct().order_by('meals')
    stars = Tour.objects.values_list('stars', flat=True).distinct().order_by('-stars')

    print(agencies)
    if request.method == 'POST':
        search_param = {
            'date': request.POST['date'],
            'country': request.POST['dest_country'],
            'stars': list(map(int, request.POST.getlist('stars'))),
            'agencies': request.POST.getlist('agencies'),
            'meals': request.POST.getlist('meals'),
            'min_price': request.POST['min_price'],
            'max_price': request.POST['max_price'],
            'sort': request.POST['sort']
        }
        tours_list = Tour.objects.filter(
            price__date=search_param['date'],
            country=search_param['country'],
            stars__in=search_param['stars'],
            price__meals__in=search_param['meals'],
            price__agency__in=search_param['agencies'],
            price__price__range=(search_param['min_price'], search_param['max_price'])
        ).order_by(search_param['sort']).distinct()
    else:
        tours_list = Tour.objects.filter(price__date=datetime.date.today()).order_by('city')
        search_param = {
            'agencies': agencies,
            'date': datetime.date.today().__str__(),
            'meals': meals,
            'stars': stars
        }

    return render(request, 'tours/tours.html', {
        'tours': tours_list,
        'countries': countries,
        'agencies': agencies,
        'meals': meals,
        'stars': stars,
        'search_param': search_param
    })


def tour_detail(request, pk):
    tour = Tour.objects.get(id=pk)
    return render(request, 'tours/tour_details.html', {'tour': tour})


def add_review(request, pk):
    form = ReviewForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.tour_id = pk
        form.save()
    return redirect(request.META.get('HTTP_REFERER'))

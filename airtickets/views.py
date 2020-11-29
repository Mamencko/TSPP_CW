import datetime

from django.shortcuts import render
from .models import Ticket, Airport


def airtickets(request):
    airports = Airport.objects.all()
    companies = Ticket.objects.values_list('company', flat=True).distinct()
    agencies = Ticket.objects.values_list('agency', flat=True).distinct()

    if request.method == 'POST':
        search_param = {
            'departurePoint': request.POST['departurePoint'],
            'destinationPoint': request.POST['destinationPoint'],
            'departureTime': request.POST['departureTime'],
            'companies': request.POST.getlist('companies'),
            'agencies': request.POST.getlist('agencies'),
            'sort': request.POST['sort'],
            'min_price': request.POST['min_price'],
            'max_price': request.POST['max_price']
        }
        tickets = Ticket.objects.filter(
            departurePoint__code=search_param['departurePoint'][-4:-1],
            destinationPoint__code=search_param['destinationPoint'][-4:-1],
            departureTime__date=search_param['departureTime'],
            company__in=search_param['companies'],
            agency__in=search_param['agencies'],
            price__range=(search_param['min_price'], search_param['max_price'])
        ).order_by(search_param['sort'])
    else:
        tickets = Ticket.objects.filter(departureTime__date=datetime.date.today())
        search_param = {
            'companies': companies,
            'agencies': agencies,
            'departureTime': datetime.date.today().__str__()
        }

    return render(request, 'airtickets/tickets.html', {
        'tickets': tickets,
        'airports': airports,
        'companies': companies,
        'agencies': agencies,
        'search_param': search_param
    })

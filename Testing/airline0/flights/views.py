from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.urls import reverse
from .models import Flight, Passenger

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found!")    
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }) 
def book(request, flight_id):
    if request.method == "POST":
        try:
            passenger_id = int(request.POST["passengers"])
            passenger = Passenger.objects.get(pk=passenger_id)
            flight = Flight.objects.get(pk=passenger_id)
        except KeyError:
            return HttpResponseBadRequest("Bad request: no passenger chosen")
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad request: passenger does not exist")
        except ValueError:
            return HttpResponseBadRequest("Bad request: invalid passanger ID")    
        
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
    else:
        return HttpResponseBadRequest("Bad request: POST required")
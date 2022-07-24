from django.shortcuts import render
#imports for calendar functions
import calendar
from calendar import HTMLCalendar
#imports for datetimes
from datetime import datetime
from .forms import VenueForm
# lazy redirect is alternative for this:
from django.http import HttpResponseRedirect
#import db model for Events
from .models import Event, Venue

def all_events(request):
	event_list = Event.objects.all()
	return render(request, 'events/event_list.html', {
		'event_list': event_list
	})

def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	return render(request, 'events/show_venue.html', {
		'venue': venue
	})

def list_venues(request):
	venue_list = Venue.objects.all()
	return render(request, 'events/venues.html', {
		'venue_list': venue_list
	})

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_venue.html', {'form':form, 'submitted': submitted})

# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	#make first letter Uppercase
	month = month.capitalize()
	#convert month from str to int
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)
	#get current time from system
	now = datetime.now()
	# create a calendar
	cal = HTMLCalendar().formatmonth(year, month_number)
	return render(request, 'events/home.html', {
		"year": year,
		"month": month,
		"monthnumber": month_number,
		"cal": cal,
		"currentyear": now.year,
	})
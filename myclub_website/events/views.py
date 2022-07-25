from django.shortcuts import redirect, render
#imports for calendar functions
import calendar
from calendar import HTMLCalendar
#imports for datetimes
from datetime import datetime
from .forms import VenueForm, EventForm
# lazy redirect is alternative for this:
from django.http import HttpResponseRedirect
#import db model for Events
from .models import Event, Venue

def all_events(request):
	event_list = Event.objects.all().order_by('name')
	return render(request, 'events/event_list.html', {
		'event_list': event_list
	})

def add_event(request):
	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_event.html', {'form':form, 'submitted': submitted})

def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')
	return render(request, 'events/update_event.html', {
		'event': event, 'form': form
	})

def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event.delete()
	return redirect('list-events')

def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')
	return render(request, 'events/update_venue.html', {
		'venue': venue, 'form': form
	})

def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')

def search_venues(request):
	if request.method == "POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)
		return render(request, 'events/search_venues.html', {'searched':searched, 'venues':venues})
	else:
		return render(request, 'events/search_venues.html', {})

def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	return render(request, 'events/show_venue.html', {
		'venue': venue
	})

def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')
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
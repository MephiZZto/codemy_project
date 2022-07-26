from django.shortcuts import redirect, render
#imports for calendar functions
import calendar
from calendar import HTMLCalendar

from django.contrib.auth.models import User

from django.contrib import messages
#imports for datetimes
from datetime import datetime
from .forms import VenueForm, EventForm, EventFormAdmin
# lazy redirect is alternative for this:
from django.http import HttpResponseRedirect
#import db model for Events
from .models import Event, Venue
# diffrent response
from django.http import HttpResponse
# import methods for csv files
import csv
#import stuff for pdf files (needs reportlab lib to be installed)
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#import Pagination stuff
from django.core.paginator import Paginator

#generate a .pdf file
def venue_pdf(request):
	# create bytestream buffer
	buf = io.BytesIO()
	# create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)

	venues = Venue.objects.all()
	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email)
		lines.append(" ")

	for line in lines:
		textob.textLine(line)
	
	#finish file
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=True, filename='venues.pdf')


#generate .csv file
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venue.csv'

	# Create a csv writer
	writer = csv.writer(response)

	# Designate the model
	venues = Venue.objects.all()

	# Add column headings to the csv file
	writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phonenumber', 'Webaddress', 'Email Address'])

	for venue in venues:
		writer.writerow([venue, venue.address, venue.zip_code, venue.phone, venue.web, venue.email])
	
	return response

#generate txt file
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venue.txt'

	# Designate the model
	venues = Venue.objects.all()
	lines = []
	for venue in venues:
		lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email}\n\n\n')
	#lines = ["This is line 1\n",
	#		 "This is line 2\n",
	#		 "This is line 3\n"]
	response.writelines(lines)
	return response

def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		events = Event.objects.filter(attendees=me)
		return render(request, 'events/my_events.html', {
			'events': events
		})
	else:
		messages.success(request, ("You are not Logged in!"))
		return redirect('home')

def search_events(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(name__contains=searched)
		return render(request, 'events/search_events.html', {'searched':searched, 'events':events})
	else:
		return render(request, 'events/search_events.html', {})

def all_events(request):
	event_list = Event.objects.all().order_by('name')
	return render(request, 'events/event_list.html', {
		'event_list': event_list
	})

def add_event(request):
	submitted = False
	if request.method == "POST":
		#user.id also works or any other field user.isadmin
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				#add an user id automaticly
				event = form.save(commit=False)
				event.manager = request.user #logged in user name
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
	else:
		# Just going to page (not submitted)
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_event.html', {'form':form, 'submitted': submitted})

def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')
	return render(request, 'events/update_event.html', {
		'event': event, 'form': form
	})

def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if event.manager == request.user:
		event.delete()
		messages.success(request, ("Event Deleted!"))
		return redirect('list-events')
	else:
		messages.success(request, ("Access Denied!"))
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
	user = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', {
		'venue': venue,
		'user': user
	})

def list_venues(request):
	#venue_list = Venue.objects.all().order_by('name')

	# set up Pagination
	p = Paginator(Venue.objects.all(), 1)
	page = request.GET.get('page')
	venues = p.get_page(page)

	#make string with length of chars equal to page num to then loop in frontend through stringlength (kinda wonky)
	nums = "a" * venues.paginator.num_pages
	return render(request, 'events/venues.html', {
		'venues': venues,
		'nums': nums
	})

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			#add an user id automaticly
			venue = form.save(commit=False)
			venue.owner = request.user.id #logged in user id
			venue.save()
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

	#Query the events model for dates
	event_list = Event.objects.filter(
		event_date__year = datetime.now().year,
		event_date__month = month_number
	)
	return render(request, 'events/home.html', {
		"year": year,
		"month": month,
		"monthnumber": month_number,
		"cal": cal,
		"currentyear": now.year,
		"event_list": event_list,
	})
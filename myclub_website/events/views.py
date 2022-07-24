from django.shortcuts import render
#imports for calendar functions
import calendar
from calendar import HTMLCalendar
#imports for datetimes
from datetime import datetime

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
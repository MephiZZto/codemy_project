from django import forms
#import forms for Models from models.py
from django.forms import ModelForm
from .models import Venue, Event

# Create a venue form
class VenueForm(ModelForm):
	#deffine what to do
	class Meta:
		model = Venue
		#fields = "__all__"
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email', 'venue_image')

		#style form sheet with lable is 
		labels = {
			'name': 'Venue Name (Lable)',
			'address': '',
			'zip_code': '',
			'phone': '',
			'web': '',
			'email': '',
			'venue_image': '',
		}
		#style form sheet with css where attrs are html element attributes like class="form-control"
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
			'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
			'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone number'}),
			'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website'}),
			'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'E-Mail Address'}),
		}

#User Event Form
class EventForm(ModelForm):
	#deffine what to do
	class Meta:
		model = Event
		#fields = "__all__"
		fields = ('name', 'event_date', 'venue', 'attendees', 'description',)

		#styleform: lable Value
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Venue',
			'attendees': 'Attendees',
			'description': '',
		}
		#style form sheet with css where attrs are html element attributes like class="form-control"
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Date'}),
			'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}

#Admin form
class EventFormAdmin(ModelForm):
	#deffine what to do
	class Meta:
		model = Event
		#fields = "__all__"
		fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description',)

		#styleform: lable Value
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Venue',
			'manager': 'Manager',
			'attendees': 'Attendees',
			'description': '',
		}
		#style form sheet with css where attrs are html element attributes like class="form-control"
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Date'}),
			'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
			'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}
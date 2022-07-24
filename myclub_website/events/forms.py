from django import forms
#import forms for Models from models.py
from django.forms import ModelForm
from .models import Venue

# Create a venue form
class VenueForm(ModelForm):
	#deffine what to do
	class Meta:
		model = Venue
		#fields = "__all__"
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email',)

		#style form sheet with lable is 
		labels = {
			'name': 'Venue Name (Lable)',
			'address': '',
			'zip_code': '',
			'phone': '',
			'web': '',
			'email': '',
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
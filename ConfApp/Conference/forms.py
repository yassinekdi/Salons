from django import forms
from django.contrib.auth import authenticate
from .models import Conference
from crispy_forms.helper import FormHelper

class DateInput(forms.DateInput):
    input_type = 'date'


class Conf_registration(forms.Form):

    # we remove labels
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


    name = forms.CharField(max_length=100)
    starting_date = forms.DateTimeField(widget=DateInput)
    finishing_date = forms.DateTimeField(widget=DateInput)
    conf_webpage = forms.CharField()
    program_webpage = forms.CharField()



# class TodoForm(forms.Form):
#     text = forms.CharField(max_length=40,
#                            widget=forms.TextInput(
#                                attrs={'class': 'form_control', 'placeholder': 'Enter todo', 'arial-label': 'Todo'}
#                            ))
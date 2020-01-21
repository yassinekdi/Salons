from django import forms
from django.forms import formset_factory

from crispy_forms.helper import FormHelper

class Conf_registration(forms.Form):

    # we remove labels
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


    name = forms.CharField(max_length=100)
    starting_date = forms.DateTimeField(widget=forms.DateInput(attrs={'id': 'starting_date', 'width': '270'}))
    finishing_date = forms.DateTimeField(widget=forms.DateInput(attrs={'id': 'finishing_date', 'width': '270'}))
    conf_webpage = forms.CharField()
    program_webpage = forms.CharField()



class Theme_form(forms.Form):

    # we remove labels
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


    theme_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': "form-control",
            'placeholder': 'Theme title',
            'style': 'width: 800px;'
        }))

Theme_formset = formset_factory(Theme_form, extra=1)





















 # <input id="datepicker" width="270" />



# class TodoForm(forms.Form):
#     text = forms.CharField(max_length=40,
#                            widget=forms.TextInput(
#                                attrs={'class': 'form_control', 'placeholder': 'Enter todo', 'arial-label': 'Todo'}
#                            ))
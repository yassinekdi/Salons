from django import forms

from crispy_forms.helper import FormHelper


class update_status_form(forms.Form):

    # we remove labels
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


    is_staff = forms.BooleanField()
    is_organizer = forms.BooleanField()
    is_chair = forms.BooleanField()
    is_speaker = forms.BooleanField()


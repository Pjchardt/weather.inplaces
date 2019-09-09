from django import forms

class NameForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=64)

class WeatherForm(forms.Form):
    location = forms.CharField(label='Location', max_length=64)

class DeleteForm(forms.Form):
    child_id = forms.CharField(widget = forms.HiddenInput(), required = False)

class LogoutForm(forms.Form):
    child_id = forms.CharField(widget = forms.HiddenInput(), required = False)

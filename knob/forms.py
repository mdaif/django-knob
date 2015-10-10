from django import forms
from django.core.exceptions import ValidationError
import re

ips_list_regex = re.compile(
    r"^(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\n)+$")


def ips_list_validation(value):
    if not value.endswith("\n"):
        value += "\n"
    if not ips_list_regex.match(value):
        raise ValidationError("Not a list of IP addresses")


class TelnetInputForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    ips = forms.CharField(validators=[ips_list_validation])
    commands = forms.CharField()
    admin_email = forms.EmailField()
    python_shell = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(TelnetInputForm, self).clean()
        if 'ips' in cleaned_data:
            cleaned_data['ips'] = cleaned_data['ips'].splitlines()

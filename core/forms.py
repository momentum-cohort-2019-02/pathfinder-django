from django import forms


class PathfinderForm(forms.Form):
    elevation_file = forms.FileField()

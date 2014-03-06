from django import forms


class CreateTool(forms.Form):
	toolname = forms.CharField()
	description = forms.CharField()
	tooltype = forms.CharField()

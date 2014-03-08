from django import forms


class CreateTool(forms.Form):
	toolname = forms.CharField()
	description = forms.CharField()
	tooltype = forms.CharField()
	CHOICES = (('1', 'My Shed',), ('2', 'Community Shed',))
	shed = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

class ToolEditor(forms.Form):
	toolname = forms.CharField()
	description = forms.CharField()
	tooltype = forms.CharField()

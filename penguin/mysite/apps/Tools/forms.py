from django import forms

from .models import Tool

class CreateTool(forms.Form):
	toolname = forms.CharField()
	description = forms.CharField()
	tooltype = forms.CharField()
	CHOICES = (('1', 'My Shed',), ('2', 'Community Shed',))
	shed = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
	tool_pickup_arrangements = forms.CharField()
	def disable_create_things(self, tool_id):
		if(not Tool.is_tool_available(tool_id)):
			self.fields.pop('shed')
			self.fields.pop('tool_pickup_arrangements')

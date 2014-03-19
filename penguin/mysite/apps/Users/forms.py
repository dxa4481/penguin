from django import forms

class UserEditor(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)
	area_code = forms.CharField()
	email = forms.CharField()
	phone_number = forms.CharField()
	default_pickup_arrangements = forms.CharField()
	def clean(self):
		password=self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password and password != confirm_password:
			raise forms.ValidationError("passwords don't match")
		return self.cleaned_data
	def disable_register_things(self):
		self.fields.pop('username')


class Login(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class LoggedIn(forms.Form):
	def clean(self):
		return self.cleaned_data





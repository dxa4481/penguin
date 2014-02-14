from django import forms

class UserEditor(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	confirmPassword = forms.CharField(widget=forms.PasswordInput)
	areaCode = forms.CharField()
	def clean(self):
		password=self.cleaned_data.get('password')
		confirmPassword = self.cleaned_data.get('confirmPassword')
		if password and password != confirmPassword:
			raise forms.ValidationError("passwords don't match")
		return self.cleaned_data
class Login(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class LoggedIn(forms.Form):
	def clean(self):
		return self.cleaned_data

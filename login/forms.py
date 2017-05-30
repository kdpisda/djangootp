from django.forms import ModelForm
from signup.models import User

class LoginForm(ModelForm):

	class Meta:
		model = User
		fields = '__all__'

class PartialLoginForm(ModelForm):

	class Meta:
		model = User
		exclude = ['status', 'key', 'uniqueKey', 'contactNo', 'name']
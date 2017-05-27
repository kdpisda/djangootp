from django.forms import ModelForm
from .models import User

class RegisterForm(ModelForm):

	class Meta:
		model = User
		fields = '__all__'

class PartialRegisterForm(ModelForm):

	class Meta:
		model = User
		exclude = ['status', 'key', 'sessionID']
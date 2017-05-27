from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, PartialRegisterForm
from .models import User
import random
from django.core.mail import send_mail


def index(request):
	return HttpResponse("Hello World")

def register(request):
	if request.method == 'POST':
		partialForm = PartialRegisterForm(request.POST)
		if partialForm.is_valid():
			finalForm = partialForm.save(commit = False)
			finalForm.key = random.randint(9999,100000)
			finalForm.save();
			send_mail(
				'Thank you for registering',
				'Thankyou for registering with us click the link below to confirm your identity.',
				'kuldeep@codenicely.in',
				[finalForm.email],
				fail_silently=False,
			)
			return HttpResponseRedirect('/signup/verify/')
	else:
		form = PartialRegisterForm()

	return render(request, 'signup.html', {'form' : form})

def thanks(request):
	return HttpResponse('Thank You!')

def verify(request):
	return HttpResponse('verification pending!!')

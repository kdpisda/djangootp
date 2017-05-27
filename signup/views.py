from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, PartialRegisterForm
from .models import User
import random
from django.core.mail import send_mail, BadHeaderError
from django.core import mail

connection = mail.get_connection()

def index(request):
	return HttpResponse("Hello World")

def register(request):

	if request.method == 'POST':
		partialForm = PartialRegisterForm(request.POST)
		if partialForm.is_valid():
			connection.open()
			finalForm = partialForm.save(commit = False)
			finalForm.key = random.randint(9999,100000)
			message = finalForm.key
			subject = 'ThankYou'
			finalForm.save();
			fromMail = 'pisdak79@gmail.com'
			toMail = request.POST.get('email','')
			try:
				send_mail(subject,message,toMail,[fromMail])
			except BadHeaderError:
				connection.close()
				return HttpResponse('Invalid header found.')
			connection.close()
			return HttpResponseRedirect('/signup/verify/')
	else:
		form = PartialRegisterForm()

	return render(request, 'signup.html', {'form' : form})

def thanks(request):
	return HttpResponse('Thank You!')

def verify(request):
	req_uniqueKey = request.GET.get('uniqueKey','')
	req_otp = request.GET.get('otp', '')
	req_email = request.GET.get('email','')
	db_obj = User.objects.get(email=req_email)
	if db_obj.uniqueKey == req_uniqueKey:
		if db_obj.otp == req_otp:
			message = 'I found you!! :)'
		else:
			message = 'InValid Request!! :('
	else:
		message = 'InValid Request!! :('

	return render(request, 'verify.html', {'message' : message})

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, PartialRegisterForm
from .models import User
import random
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.core import mail
from django.template.loader import render_to_string	

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
			context = {'otp' : finalForm.key, 'uniqueKey':finalForm.uniqueKey, 'email':finalForm.email}
			message = render_to_string('email.html', context = context).strip()
			subject = 'Confirm your account'
			finalForm.save();
			fromMail = 'kdpisda@gmail.com'
			toMail = request.POST.get('email','')
			try:
				send_mail(subject,message,toMail,[fromMail])
			except BadHeaderError:
				connection.close()
				return HttpResponse('Invalid header found.')
			connection.close()
			redirect_url = '/signup/enterotp/?email='+finalForm.email+'&&uniqueKey='+str(finalForm.uniqueKey)
			return HttpResponseRedirect(redirect_url)
	else:
		form = PartialRegisterForm()

	return render(request, 'signup.html', {'form' : form})

def verify(request):
	if request.method == 'GET':
		req_uniqueKey = request.GET.get('uniqueKey','')
		req_otp = request.GET.get('otp', '')
		req_email = request.GET.get('email','')
		db_obj = User.objects.get(email=req_email)
		db_key = str(db_obj.uniqueKey)
		if db_key == req_uniqueKey:
			if db_obj.key == req_otp:
				if db_obj.status == 'PN':
					db_obj.status = 'AC'
					db_obj.save()
					message = 'Thankyou Your account has been activated successufully! :)'
				else:
					message = 'Your account has already been activated'
			else:
				message = 'InValid Request!!'
		else:
			message = 'Invalid Request!!!'
			return HttpResponse(message)
		return render(request, 'verify.html', {'message' : message})
	else :
		return HttpResponseRedirect('/signup/')

def enterotp(request):
	if request.method == 'GET':
		email = request.GET.get('email','')
		uniqueKey = request.GET.get('uniqueKey','')
		context = {'email': email, 'uniqueKey': uniqueKey}
		return render(request, 'enterotp.html', context)
	else:
		return HttpResponseRedirect('/signup/')
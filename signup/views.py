from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, PartialRegisterForm
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.core import mail
from django.template.loader import render_to_string	
import random

connection = mail.get_connection()

def index(request):
	try:
		if request.session.get('email','') != '':
			if request.session.get('uniqueKey','') != '':
				form = PartialRegisterForm()
				return render(request, 'index.html', {'form':form})
			else:
				return HttpResponseRedirect('/dashboard')
		else:
			form = PartialRegisterForm()
			return render(request, 'index.html', {'form':form})
	except:
		form = PartialRegisterForm()
		return render(request, 'index.html', {'form':form})

def register(request):
	try:
		if request.method == 'POST':
			partialForm = PartialRegisterForm(request.POST)
			if partialForm.is_valid():
				try:
					req_email = request.POST.get('email', '')
					email_exists = User.objects.get(email=req_email)
					context = {'message':"Sorry the email already exists plese check your email to confirm your account!!!" }
					return render(request, 'error.html',context)
				except ObjectDoesNotExist:
					connection.open()
					finalForm = partialForm.save(commit = False)
					finalForm.key = random.randint(9999,100000)
					if request.is_secure():
						secure = 'https://'
					else :
						secure = 'http://'
					host = secure + request.META['HTTP_HOST']
					context = {'otp' : finalForm.key, 'uniqueKey':finalForm.uniqueKey, 'email':finalForm.email, 'host':host}
					message = render_to_string('email.html', context = context).strip()
					subject = 'Confirm your account'
					finalForm.save();
					toMail = 'kuldeep@codenicely.in'
					fromMail = request.POST.get('email','')
					try:
						send_mail(subject,message,toMail,[fromMail])
					except BadHeaderError:
						connection.close()
						return HttpResponse('Invalid header found.')
					connection.close()
					redirect_url = '/signup/enterotp/?email='+finalForm.email+'&&uniqueKey='+str(finalForm.uniqueKey)
					return HttpResponseRedirect(redirect_url)
			else:
				context = {'message':"Form is not valid" }
				return render(request, 'error.html',context)
		else:
			context = {'message':"Request is not proper" }
			return render(request, 'error.html',context)
	except Exception as e :
		raise e
		context = {'message':"Something bad in main try" }
		return render(request, 'error.html',context)

def enterotp(request):
	try:
		if request.method == 'GET':
			try:
				if request.GET.get('email','') :
					if request.GET.get('uniqueKey',''):
						if request.GET.get('otp', ''):
							return HttpResponseRedirect('/signup/')
						else:
							email = request.GET.get('email','')
							uniqueKey =request.GET.get('uniqueKey','')
							context = {'email': email, 'uniqueKey': uniqueKey}
							return render(request, 'enterotp.html', context)
					else:
						context = {'message':"No unique key" }
						return render(request, 'error.html',context)
				else:
					context = {'message':"No email" }
					return render(request, 'error.html',context)
			except:
				context = {'message':"Sorry an error occured while processing your request" }
				return render(request, 'error.html',context)
		else:
			context = {'message':"Sorry an error occured while processing your request" }
			return render(request, 'error.html',context)
	except:
		context = {'message':"Sorry an error occured while processing your request" }
		return render(request, 'error.html',context)

def verify(request):
	try:
		if request.method == 'GET':
			req_uniqueKey = request.GET.get('uniqueKey','')
			req_otp = request.GET.get('otp', '')
			req_email = request.GET.get('email','')
			db_obj = User.objects.get(email=req_email)
			db_key = str(db_obj.uniqueKey)
			if str(db_obj.uniqueKey) == req_uniqueKey:
				if db_obj.key == req_otp:
					if db_obj.status == 'PN':
						db_obj.status = 'AC'
						db_obj.save()
						request.session['user_id'] = db_key
						request.session['email'] = req_email
						return HttpResponseRedirect('/dashboard')
					else:
						context = {'message' : 'Your account has already been activated'}
						request.session['user_id'] = str(db_obj.uniqueKey)
						request.session['email'] = db_obj.email
						return HttpResponseRedirect('/dashboard')
				else:
					context = {'message' : 'OTP problem!!'}
					return render(request, 'error.html', context)
			else:
				context = {'message' : 'Unique key problem!!'}
				return render(request, 'error.html', context)
		else :
			return HttpResponseRedirect('/signup/')	
	except:
		return HttpResponseRedirect('/signup/')	

def validate_username(request):
	email = request.GET.get('email', None)
	data = {
		'is_taken': User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)
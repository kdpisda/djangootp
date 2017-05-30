from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, PartialLoginForm
from signup.models import User
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
				form = PartialLoginForm()
				return render(request, 'login.html', {'form':form})
			else:
				return HttpResponseRedirect('/dashboard')
		else:
			form = PartialLoginForm()
			return render(request, 'login.html', {'form':form})
	except:
		return HttpResponseRedirect('/signup')

def verify(request):
	try:
		if request.session.get('email','') != '':
			return HttpResponseRedirect('/login')
		else:
			try:
				if request.method == 'GET':
					if request.GET.get('email','')=='' :
						return HttpResponseRedirect('/login')
					else:
						email = request.GET.get('email','')
						uniqueKey =request.GET.get('uniqueKey','')
						otp = request.GET.get('otp', '')
						db_obj = User.objects.get(email=email)
						if email == db_obj.email:
							if otp == db_obj.key:
								if uniqueKey == str(db_obj.uniqueKey):
									request.session['user_id'] = str(db_obj.key)
									request.session['email'] = email
									return HttpResponseRedirect('/dashboard')
								else: 
									context = {'message':"Wrong OTP" }
									return render(request, 'error.html',context)
							else:
								context = {'message':"Wrong OTP" }
								return render(request, 'error.html',context)
						else:
							context = {'message':"Wrong OTP" }
							return render(request, 'error.html',context)
			except:
				context = {'message':"An error occured while processing your request" }
				return render(request, 'error.html',context)
	except:
		return HttpResponseRedirect('/login')

def enterotp(request):
	try:
		if request.method == 'POST':
			if request.POST.get('email','') == '':
				context = {'message':"NO post data" }
				return render(request, 'error.html',context)
			else:
				tempUser = User.objects.get(email = request.POST.get('email',''))
				tempUser.key = random.randint(9999,100000)
				tempUser.save()
				connection.open()
				context = {'otp': tempUser.key}
				message = render_to_string('email_message.html', context = context).strip()
				subject = 'OTP for login'
				toMail = 'kuldeep@codenicely.in'
				fromMail = request.POST.get('email','')
				try:
					send_mail(subject,message,toMail,[fromMail])
				except BadHeaderError:
					connection.close()
					return HttpResponse('Invalid header found.')
				connection.close()
				context = {'email':tempUser.email, 'uniqueKey':tempUser.uniqueKey}
				return render(request, 'login_verify.html', context)
		else:
			context = {'message':"invld request" }
			return render(request, 'error.html',context)
	except:
		return HttpResponseRedirect('/login')
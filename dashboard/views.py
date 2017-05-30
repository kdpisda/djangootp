from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	try:
		if request.session.get('email','') != '':
			if request.session.get('uniqueKey','') != '':
				return HttpResponseRedirect('/login')
			else:
				context = {'email':request.session.get('email','')}
				return render(request, 'dashboard.html', context)
		else:
			return HttpResponseRedirect('/login')
	except:
		return HttpResponseRedirect('/signup')

def logout(request):
	try:
		if request.session.get('email','') != '':
			if request.session.get('uniqueKey','') != '':
				return HttpResponseRedirect('/login')
			else:
				del request.session['user_id']
				del request.session['email']
				context = {'message': 'Logged out successfully'}
				return render(request, 'message.html', context)
		else:
			return HttpResponseRedirect('/login')
	except:
		return HttpResponseRedirect('/login/')
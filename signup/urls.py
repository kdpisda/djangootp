from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register, name='index'),
    url(r'^register/', views.register, name='index'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^verify/', views.verify, name='verify'),
]
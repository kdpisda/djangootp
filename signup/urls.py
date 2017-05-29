from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register, name='index'),
    url(r'^register/', views.register, name='index'),
    url(r'^verify/', views.verify, name='verify'),
    url(r'^enterotp/', views.enterotp, name='enterotp'),
]
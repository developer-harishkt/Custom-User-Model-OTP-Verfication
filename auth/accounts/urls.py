from django.urls import path
from . import views
from django.conf.urls import url
from knox import views as know_views

urlpatterns = [
    path('validate_phone', views.ValidatePhoneSendOTP.as_view()),
    path('validate_otp', views.ValidateOTP.as_view()),
    path('register', views.Register.as_view()),
    url(r'^login/$', views.LoginAPI.as_view()),
    url(r'^logout/$', know_views.LogoutView.as_view()),
]

from django.urls import path

from user.views import Register, Login, ForgetPass, UpdateProfile, UpdatePass

app_name = 'user'
urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('forget_pass', ForgetPass.as_view(), name='forget_pass'),
    path('update_pass', UpdatePass.as_view(), name='forget_pass'),
    path('update_profile', UpdateProfile.as_view(), name='update_profile'),
]
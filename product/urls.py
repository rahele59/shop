from django.urls import path

from product import views

app_name = 'product'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),

]
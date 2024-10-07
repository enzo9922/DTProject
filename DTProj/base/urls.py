from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('bidding/<str:bidding_url>/', views.bidding, name="bidding"),
    path('agreement/<str:bidding_url>/', views.agreement, name="agreement"),
    path('auction/<str:bidding_url>/', views.auction, name="auction"),
    path('submit-form/', views.submit_form, name='submit_form'),

]
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name="shophome"),
    path('about/',views.about,name="AboutUs"),
    path('contact/',views.contact,name="ContactUs"),
    path('search/',views.search,name="Search"),
    path('tracker/',views.tracker,name="Tracking status"),
    path('Products/<int:myid>',views.productView,name="Products"),
    path('checkout/',views.checkout,name="Checkout"),
    path('handlerequest/',views.handlerequest,name="handlerequest")
   
    
    
]
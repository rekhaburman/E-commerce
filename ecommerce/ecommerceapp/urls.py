from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),  # Updated to match the correct view function
    path('about/', views.about, name='about'),
    path('checkout/',views.checkout_view,name='checkout'),
    path('payment/',views.payment_execute,name='payment')
]

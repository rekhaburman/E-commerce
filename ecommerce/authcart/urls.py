from django.urls import path
from authcart import views  # Make sure views is correctly imported

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    
   
]

from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login as auth_login, logout  
from django.contrib import messages  
from django.conf import settings 

# Optional based on your use case:
from django.views.generic import View 
from django.contrib.auth.decorators import login_required  





def signup(request):
    if request.method=='POST':  
        print(request.POST)
               
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request,"password is Not Matching")
            return render(request,'signup.html')
        try:
            if User.objects.get(username=email):
                messages.info(request,"Email is Taken")
                # return HttpResponse("email already exist")
                return render(request,'signup.html')
        except Exception as identifier:
        # If an exception occurs (e.g., no user found), ignore the exception and proceed
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                return redirect(request,'signup.html')
        except Exception as identifier:
            pass    

        user=User.objects.create_user(email,email,password)
        user.save()
        messages.info(request,'Thanks For Signing Up')

        # return HttpResponse("User created",email)
    return render(request,"signup.html")

def login_view(request):  
    if request.method == 'POST':
        # Get parameters from the form
        loginusername = request.POST.get('email')  
        loginpassword = request.POST.get('pass1')

        user = authenticate(username=loginusername, password=loginpassword)
       
        if user is not None:
            auth_login(request, user)  
            # messages.info(request, "Successfully Logged In")
            return redirect('/') 

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')  
    return render(request, 'login.html')       

 

def logout_view(request):
    logout(request)
    messages.warning(request,"Logout Success")
    return render(request,'login.html')
    


from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm



# Create your views here.
def home(request):
    return render(request, 'users/home.html')



def user_logout(request):

   messages.success(request, 'You logged out') 
   logout(request)
   return redirect("home")



def register(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() :
           user = form.save()
          
       

           login(request, user)

           return redirect("home")

    context = {
     'form':form,
    }
    return render(request, "users/register.html", context) 

def user_login(request):
    form = AuthenticationForm(request, data=request.POST) # data=> metormhod post ise fu dolduruyor, auth forma ait bir özellik

    if form.is_valid():
        user = form.get_user()
        #get_user authform a ait bir özellik

      
        
        if user:
          
            login(request, user)
            return redirect('home')
    

    return render(request, 'users/user_login.html', {'form': form}) 

def profile_page(request):
    profile = UserCreationForm(request.POST)

    return render(request, 'users/profile_page.html', {'profile': profile})


### USER REGISTER
<hr>

1. Yöntem, 

Django'nun default gelen user tablosu ile kayıt oluşturma, 
  
   *** bu durumda iki farklı secenek ile ilerlenebilir
      
     # a.  forms.py oluşturarak ilerleme #

forms.py  =>

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User # user ı kullan ve sadece username ve email aldık
        fields= ('username', 'email')



views.py =>


from .forms import UserForm

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


     # b.  views.py içinde user oluşturarak ilerleme #

*** bu yöntemde forms.py oluşturmadık!!!!

from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() :
           user = form.save()
          
       

           login(request, user)

           return redirect("home")

    context = {
     'form':form,
    }
    return render(request, "users/register.html", context) 


**** YUKARIDAKİ HER İKİ YÖNTEM DE REGISTER.HTML SAYFASINA YÖNLENDİRDİK ****

###   USER LOGOUT 

from django.contrib.auth import  logout


def user_logout(request):

   messages.success(request, 'You logged out') 
   logout(request)
   return redirect("home")


LOGOUT İSLEMİNDE TEMPLATE SAYFA OLUŞTURMAYA GEREK YOK  



### USER LOGIN

from django.contrib.auth.forms import AuthenticationForm

Login işleminde AuthenticationForm import ediyoruz

def user_login(request):
    form = AuthenticationForm(request, data=request.POST) 
    # forma istenilen değerleri verdik, normalde formu boş alıp requesti içine koyuyoruz, burada auth forma ait bir özellikten faydalandık, data=> method post ise formu dolduruyor

    if form.is_valid():
         
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        # user = authenticate(username=username, password = password)
       
        kayıtlı kullanıcıyı yakalabilmek için yukarıdaki üc satırlık kod yazılabilirdı, fakat biz form.get_user() ile bu üc komutta yapılacak işlemi yaptık

        user = form.get_user()
        #get_user authform a ait bir özellik

      
        
        if user:
          
            login(request, user)
            return redirect('list')
    

    return render(request, 'users/user_login.html', {'form': form}) 



# pythonanywhere

# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/kale11/mysite/mysite/settings.py'
# and your manage.py is is at '/home/kale11/mysite/manage.py'
path = '/home/kale11/word_app'  => source kod
if path not in sys.path:
   sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'  => proje ismi

## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
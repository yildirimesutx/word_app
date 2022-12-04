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



### CRUD ###


1. Models.py oluşturma:

ihtiyacımız olan ve database'e aktarılması gereken tabloları burada hazırlıyoruz, ayrıca birden fazla tablo oluşturulacaksa, bu tabloları relationship methodları ile ilişkilendirilmesi gerekiyor

example : aşağıda bu üç ilişkiyi kuracağımız bir tablo yazalım,

bir yazar düşünelim sadece bir progalama dili yazabiliyor(python->Guido gibi), budurumda bir dile bir yazar onetoone modeli, 
yazılan dilin birden çok frameworku olabiliyor (python-> django, flask..) bu durumda da manytoone oluyor. burdaki freamworklerin başka bir dile ait olmaması gerekiyor, tek bir dile ait olacaklar 

Bu frameworkleri bilen bir çok developer olabilir, aynı zamanda bu frameworklerin ait olduğu bir çok developer olabilir şeklinde düşünebiliriz.

   a. One-to-one relationships



class Creator(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.first_name
    
    
class Language(models.Model):
    name = models.CharField(max_length=50)
    yazarı = models.OneToOneField(Creator, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name




   b. Many-to-one relationships

bağlantı kurulacak bir çok yapıyı ForeignKey ile tek olan yapıyla ilişkilendirdik

class Frameworks(models.Model):
    name = models.CharField(max_length=50)
    Language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


   c. Many-to-Many relationships

burada bir developer birden çok framework u bilebilir, bir frameworkte birden çok developera tarafından öğrenilebilir şeklinde düşünebiliriz

class Developers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    frameworks = models.ManyToManyField(Frameworks)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

2. Oluşturmuş olduğumuz bu tabloları  models.py daki, kullanıcıların doldurması için forms.py da çağırdık
model yapısında kullandığımız ve forms sayfasında kullanmayacağımız attributlari exclude ile ayırdık

forms.py

from .models import NewPost, Comments

from django import forms


class NewPostForm(forms.ModelForm):
    class Meta:
        model = NewPost
        # fields = '__all__'
        exclude = ('user', 'post_view', 'post_like','comment_number' )

class CommentForm(forms.ModelForm): 
    class Meta:
        model = Comments
        # fields = '__all__'       
        exclude = ('post',)



3. CREATE 

CREATE işleminde kullanıcıdan bilgi girişi yapabilmesi için forms.py daki formumuzu çağırdık,
formu çekip template gönderdik,1.

 1.aşama : formu boş çağırdık
def newpost_add(request):
    form = NewPostForm() 
    
    #print(request.POST) ile forma yazdığımız içeriği alabiliyoruz.

    context = {
       "form":form
    }

    return render(request, "blog/newpost_add.html", context)


  2. aşama : formu doldurma ve DB gönderme
def newpost_add(request):

   <!-- form = NewPostForm(request.POST or None, request.FILES or None) -->
    <!-- bu yazım şekli aşağıda belirilen üç satır yenine geçiyor -->

   form = NewPostForm() 
    
   if request.method == "POST":
      form = NewPostForm(request.POST, request.FILES)
      # forma request post ekledik, form içinde dosya gönderildiği içinde request.FILES ekledik, 

       if form.is_valid():
       #form un dolu olduğunu kontrol ettik
       #formu yeni bir değişkene atatık, formu direk DB göndermemek için commit=False yaptık, 
       modelde user ile ilişkilendirdiğimiz tablo olduğu için ve biz bu userları, kullnıcı tarafından doldurulmamasını ve görmemesini istediğimiz için formda user attributünü göndermedik,
       fakat oluşturulacak yazı/blog/post ile userı ilişkilendirilmesi gerekiyor. commit=False ile DB göndermediğimiz formu yakalayıp user attributunu request user a eşitledik ve sonra formu save ettik

          newform = form.save(commit=False)
          newform.user = request.user
          newform.save()
          return redirect("list")
                 <!-- redirect("blog:list") burada urls.py da app_name = "blog" birden fazla app olması ve name lerin aynı olması durumunda çakışma olmaması için kullanılıyor -->

    context = {
       "form":form
    }

    return render(request, "blog/newpost_add.html", context)


4. READ 

model den alıp içini doldurduğumuz tabloyu aşağıdaki gibi çağırdık, eğer yazılan postlların bazılarını durumuna göre public, private yapsaydık, yani model sayfasından post yayınlanırken böle bir girdi isteseydik, burada sadece public leri göstermemiz gerekeçekti, burada 

post= Post.objects.filter(status='p') bu şekilde çağırmamız gerekirdi, buradaki status attribut ve p de choise olarak db göndderilen

def post_list(request):

    post = NewPost.objects.all()

    context = {
       'post' : post,

    }

    return render(request, 'blog/post_list.html', context)


5. UPDATE   

    modeldeki classı çağırdk, id ile, get(id=id) ile, güncelleme işlemini yapılabilmesi için kayıtlı bilgileride getirmemiz gerekiyor, kayıtlıbilgileri forma ekrana getirmemiz gerekiyor, instance=post ile getirdik,

    çağırdığımız formu geri göndeririken  method un post olduğunu kontrol ederek geri gönderdik

def post_update(request, id):
    post = NewPost.objects.get(id=id)
    form = NewPostForm(instance=post)

    if request.method == 'POST':
       form = NewPostForm(request.POST,  request.FILES or None, instance=post)
       if form.is_valid():
           form.save()

           return redirect("list")

    context = {
        "form" : form
    }       

    return render(request, "blog/post_update.html", context)  



6. DELETE       

def post_delete(request, id):
    post = NewPost.objects.get(id=id)

    if request.method =='POST':
        post.delete()

        return redirect("list")

    context= {
        'post':post
    } 

    return render(request, 'blog/post_delete.html', context)   

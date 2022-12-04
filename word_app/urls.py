from django.urls import path
from .views import home, delete_city, list, about 

urlpatterns = [
    path('', home, name="home"),
    path('list/', list, name="list"),
    path('about/', about, name="about"),
    path('delete/<int:id>', delete_city, name="delete")
   
]
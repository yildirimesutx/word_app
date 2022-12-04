
from django.urls import path
from .views import home, register, user_logout, user_login, profile_page

urlpatterns = [
    # path('', home, name="home"),
    path('logout', user_logout, name="logout"),
    path('register', register, name="register"),
    path('login', user_login, name="user_login"),
    path('profile', profile_page, name="profile"),
] 
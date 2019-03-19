
from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

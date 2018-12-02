from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('words/',views.index,name="words-index"),
    path('words/<str:word_name>/', views.detail, name='words-detail'),
]

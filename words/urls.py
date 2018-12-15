from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="words-index"),
    path('words/',views.index,name="words-index"),
    path('random/',views.get_random,name="random"),
    path('words/<str:word_name>/', views.detail, name='words-detail'),
    path('words/add/<str:word_name>', views.add_word, name="words-add_word_details"),
    # path('add/',views.add,name="words-add_action"),
]

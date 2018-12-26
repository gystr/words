from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="words-index"), #index homePage
    path('words/',views.index,name="words-index"),#index homePage
    path('random/',views.get_random,name="random"), #Random word
    path('words/<str:word_name>/', views.detail, name='words-detail'), # detail page
    path('words/add/<str:word_name>', views.add_word, name="words-add_word_details"),# add word page
    path('about/',views.about,name="about-page"),
    path('contact/',views.contact,name="contact"),
    path('tag/<str:str_Tag>',views.tag_page,name="tag-detail-page"),
]

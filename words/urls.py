from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('',views.index,name="words-index"), #index homePage
    path('words/',views.index,name="words-index"),#index homePage
    path('random/',views.get_random,name="random"), #Random word
    path('words/<str:word_name>/', views.detail, name='words-detail'), # detail page
    path('words/add/<str:word_name>', views.add_word, name="words-add_word_details"),# add word page
    path('add/', views.add_word, name="words-add_word_details"),
    path('about/',views.about,name="about-page"), #about page
    path('contact/',views.contact,name="contact"), #contact page
    path('tag/<str:str_Tag>',views.tag_page,name="tag-detail-page"), #Tag page for words of a certain tag
    path('tagList/', views.all_tags, name="all-tags-page"), #page where all tags are displayed
    path('signup/', views.signup, name="signup"), #page where all tags are displayed
    # repath('activate/<str:uidb64>/<str:token>',views.activate, name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

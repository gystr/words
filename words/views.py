from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Word
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect

from django.db.models import Max
import random
# Create your views here.

def index(request):
    if request.method == 'POST': # If the form is submitted with POST
         search_query = request.POST.get('query', None) # Get query from form
         return HttpResponseRedirect('/words/'+ str(search_query)) # Return redirect to .detail
    else: # Else display regular index page
        word_list = Word.objects.all()
        return render(request, 'words/index.html',{'word_list': word_list})

# def detail(request,word_name):
#     word = get_object_or_404(Word, word_name=word_name)
#     return render(request, 'words/detail.html', {'word': word})

def detail(request,word_name):
    try: #Try to find the word that was provided in the URl
        word = Word.objects.get(word_name=word_name)
        return render(request, 'words/detail.html', {'word': word})
    except Word.DoesNotExist:#Except error and redirect to /words/add/+query
        return HttpResponseRedirect('/words/add/'+ str(word_name))
    except:# If another error occurs Return404 ¯\_(ツ)_/¯
        return Http404("An Error Has Occured At Detail Page!")

def get_random(request):
        max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            category = Word.objects.filter(pk=pk).first()
            if category:
                return HttpResponseRedirect('/words/'+ str(category.word_name))

def add_word(request,word_name):
    return render(request, 'words/addWord.html',{'word_name': word_name})

# def add(request):

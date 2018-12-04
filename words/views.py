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
    if request.method == 'POST': # If the form is submitted
         search_query = request.POST.get('query', None)
         return HttpResponseRedirect('/words/'+ str(search_query))
    else:
        word_list = Word.objects.all()
        return render(request, 'words/index.html',{'word_list': word_list})

def detail(request,word_name):
    word = get_object_or_404(Word, word_name=word_name)
    return render(request, 'words/detail.html', {'word': word})

def get_random(request):
        max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            category = Word.objects.filter(pk=pk).first()
            if category:
                return HttpResponseRedirect('/words/'+ str(category.word_name))

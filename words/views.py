from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Word
from django.shortcuts import redirect, reverse
# Create your views here.

def index(request):
    # if request.method == 'GET': # If the form is submitted
    #     search_query = request.GET.get('search_box', None)
    #     return redirect(reverse('words/') + search_query)

    word_list = Word.objects.all()
    return render(request, 'words/index.html',{'word_list': word_list})

def detail(request,word_name):
    word = get_object_or_404(Word, word_name=word_name)
    return render(request, 'words/detail.html', {'word': word})

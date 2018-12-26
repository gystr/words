from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Word, Tag
from .forms import WordForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
import random
# Create your views here.



def index(request):
    if request.method == 'POST': # If the form is submitted with POST
         search_query = request.POST.get('query', None) # Get query from form
         return HttpResponseRedirect('/words/'+ str(search_query)) # Return redirect to .detail
    else: # Else display regular index page
        word_list = Word.objects.all()[:10]
        other_words = Word.objects.order_by('-upvotes')[:5]
        return render(request, 'words/index.html',{'word_list': word_list,'other_words' : other_words})








def detail(request,word_name):
    try: #Try to find the word that was provided in the URl
        words = Word.objects.filter(word_name=word_name)
        if not words: #if the word_set in None redirect to add_word
            return HttpResponseRedirect('/words/add/'+ str(word_name))
        else:
            return render(request, 'words/detail.html', {'words': words})
    except Word.DoesNotExist:#Except error and redirect to /words/add/+query
        return HttpResponseRedirect('/words/add/'+ str(word_name))
    except AttributeError:# If another error occurs Return404 ¯\_(ツ)_/¯
        return Http404("An Error Has Occured At Detail Page!")





def get_random(request):
        max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            category = Word.objects.filter(pk=pk).first()
            if category:
                return HttpResponseRedirect('/words/'+ str(category.word_name))







def add_word(request,word_name):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['word_name']
            defi = form.cleaned_data['word_def']
            exmp = form.cleaned_data['word_example']
            tags = form.cleaned_data['word_tags']

            w = Word(word_name=name,word_def=defi,word_example=exmp,pub_date=timezone.now())
            w.save()
            messages.info(request, 'word has been added to Database!')
            return HttpResponseRedirect('/')
    else:
        form = WordForm()
    return render(request, 'words/addWord.html',{'word_name': word_name,'form': form})


def tag_page(request,str_Tag):
    t = Tag.objects.get(tag_name=str(str_Tag))
    tagged_words = Word.objects.filter(word_tag=t)
    return render(request, 'words/tag.html',{'t': t,'tagged_words':tagged_words})

def about(request):
    return render(request, 'words/about.html')


def contact(request):
    return render(request, 'words/contact.html')

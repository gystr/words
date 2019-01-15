from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Word, Tag
from .forms import WordForm, ContactForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
import random
from django.core.mail import send_mail, BadHeaderError
# Create your views here.



def index(request):
    if request.method == 'POST': # If the form is submitted with POST
         search_query = request.POST.get('query', None) # Get query from form
         return HttpResponseRedirect('/words/'+ str(search_query)) # Return redirect to .detail
    else: # Else display regular index page
        pop_tags = Tag.objects.all()[:32]
        other_words = Word.objects.order_by('-upvotes')[:20]
        return render(request, 'words/index.html',{'other_words' : other_words,'pop_tags' : pop_tags})








def detail(request,word_name):
    try: #Try to find the word that was provided in the URl
        words = Word.objects.filter(word_name=word_name).order_by('-upvotes')
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            _from = form.cleaned_data['from_email']
            _subject = form.cleaned_data['subject']
            _message = form.cleaned_data['message']

            try:
                send_mail(_subject, _message, _from, ['sternshos@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect('/')
    else:
        form = ContactForm()
    return render(request, 'words/contact.html',{'form': form})

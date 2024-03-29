from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Word, Tag
from .forms import WordForm, ContactForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from users.models import Profile
import random
import json
from .misc import normalized_word


def index(request):
    if request.method == 'POST': # If the form is submitted with POST
         search_query = request.POST.get('query', None) # Get query from form
         return HttpResponseRedirect('/words/'+ str(search_query)) # Return redirect to .detail
    else: # Else display regular index page
        pop_tags = Tag.objects.all()[:34]
        other_words = Word.objects.order_by('-num_vote_up')[:12]
        return render(request, 'words/index.html',{'other_words' : other_words,'pop_tags' : pop_tags})








def detail(request,word_name):
    try: #Try to find the word that was provided in the URl
        clean_word = normalized_word(word_name)
        words = Word.objects.filter(filtered_word=clean_word).order_by('-num_vote_up')
        if not words: #if the word_set in None redirect to add_word
            return HttpResponseRedirect('/words/add/'+ str(word_name))
        else:
            paginator = Paginator(words, 4)
            page = request.GET.get('page')
            contacts = paginator.get_page(page)
            return render(request, 'words/detail.html', {'words': contacts})
    except Word.DoesNotExist:#Except error and redirect to /words/add/+query
        return HttpResponseRedirect('/words/add/'+ str(word_name))
    except AttributeError:# If another error occurs Return404 ¯\_(ツ)_/¯
        return Http404("An Error Has Occured At Detail Page!")





def get_random(request):
        max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id'] #max amount of words
        while True:
            pk = random.randint(1, max_id) # random number between 1 and max amount of words
            category = Word.objects.filter(pk=pk).first() # get words of assosicated with pk
            if category: # if word is valid send url
                return HttpResponseRedirect('/words/'+ str(category.word_name))



def add_word(request,word_name="מלא את הטופס:"):
    if request.method == 'POST' and request.user.is_authenticated:  # If the form is submitted with POST and the request is by an auth user
        form = WordForm(request.POST)
        if form.is_valid() and request.user.profile.can_publish(): #If the form is valid and the function can publish returns True save form data
            name = form.cleaned_data['word_name']
            defi = form.cleaned_data['word_def']
            exmp = form.cleaned_data['word_example']
            tags = form.cleaned_data['word_tags']
            cur_user = request.user
            clean_word = normalized_word(name)
            w = Word(author=cur_user,word_name=name,filtered_word=clean_word,word_def=defi,word_example=exmp,pub_date=timezone.now())
            w.save() # save word
            cur_user.profile.published_words.add(w) # add word to the user's published words
            w.save() # save again for some reason
            tag_list = str(tags).split(",") # get tags from form
            if str(tags) == "": # if tag list is empty pass NOT WORKING!!!
                pass
            else:
                for str_t in tag_list:
                    try:
                        t = Tag.objects.get(tag_name=str(str_t))
                        w.word_tag.add(t)
                    except:
                        t = Tag(tag_name=str(str_t),tag_slug=str("tagSlug"))
                        t.save()
                        w.word_tag.add(t)

            messages.info(request, 'word has been added to Database!')
            return HttpResponseRedirect('/')
    else:
        form = WordForm()
    return render(request, 'words/addWord.html',{'word_name': word_name,'form': form})


def tag_page(request,str_Tag):
    t = Tag.objects.get(tag_name=str(str_Tag))
    tagged_words = Word.objects.filter(word_tag=t)
    paginator = Paginator(tagged_words, 6)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'words/tag.html',{'t': t,'tagged_words':contacts})


def all_tags(request):
    all_tags = Tag.objects.all().order_by('tag_name')
    all_letters = ["א","ב","ג","ד","ה","ו","ז","ח","ט","י","כ","ל","מ","נ","ס","ע","פ","צ","ק","ר","ש","ת"]
    return render(request,'words/allTags.html',{'all_tags' : all_tags,"all_letters": all_letters})

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
                msg = send_mail(_subject, _message, _from, ['slangs.website@gmail.com'],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect('/')
    else:
        form = ContactForm()
    return render(request, 'words/contact.html',{'form': form})


def vote(request,slug,direction):
    result = None
    if request.method == 'POST' and request.user.is_authenticated:
        w = Word.objects.get(pk=slug)
        user_profile = Profile.objects.get(user=request.user)
        print(user_profile)
        if user_profile.can_vote(w):
            if direction == "upvote":
                w.num_vote_up += 1
                print("upvoted")
            else:
                w.num_vote_down += 1

            user_profile.voted_words.add(w)
            print("word added!")
            user_profile.save()
            print("word saved!")
            w.save()
            result = {
                'success': True
                    }

    if request.method == 'POST' and not request.user.is_authenticated:
        result = {
            'success': False,
            'message' : "עליך להיות משמתמש רשום בכדי להצביע!"
                }
    return HttpResponse(json.dumps(result), content_type="application/json")

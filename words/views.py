from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Word, Tag
from .forms import WordForm, ContactForm, SignupForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
import random
from django.core.mail import send_mail, BadHeaderError
# Create your views here.

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage





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
        max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id'] #max amount of words
        while True:
            pk = random.randint(1, max_id) # random number between 1 and max amount of words
            category = Word.objects.filter(pk=pk).first() # get words of assosicated with pk
            if category: # if word is valid send url
                return HttpResponseRedirect('/words/'+ str(category.word_name))



def add_word(request,word_name="מלא את הטופס:"):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['word_name']
            defi = form.cleaned_data['word_def']
            exmp = form.cleaned_data['word_example']
            tags = form.cleaned_data['word_tags']

            w = Word(word_name=name,word_def=defi,word_example=exmp,pub_date=timezone.now())
            w.save()
            tag_list = str(tags).split(",")
            if not tag_list:
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
    return render(request, 'words/tag.html',{'t': t,'tagged_words':tagged_words})


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
                msg = send_mail(_subject, _message, _from, ['sternshos@gmail.com'],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return redirect('/')
    else:
        form = ContactForm()
    return render(request, 'words/contact.html',{'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Salngs account.'
            message = render_to_string('words/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'words/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

import csv
from words.models import Word,Tag
from django.utils import timezone
from django.contrib.auth.models import User
import unicodedata

def normalized_word(string_of_word):
    nikudnik = str(string_of_word)
    normalized = unicodedata.normalize('NFKD', nikudnik)
    flattened = "".join([c for c in normalized if not unicodedata.combining(c)])
    return flattened

try:
    Default_User = User.objects.get(pk=1)
except:
    Default_User = User()
    Default_User.save()

def add_words(db_path = r'D:\programming\testingjs\fuckingKillHebrew\words.csv'):
    with open(db_path ,encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            no_nikkud_word = normalized_word(row['word'])
            w = Word(author=Default_User,word_name=row['word'],filtered_word=no_nikkud_word, word_def=row['descrepition'],
            word_example=row['example'],pub_date=timezone.now())

            w.save()
            tag_list = row['Tag'].split(',')

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

add_words()
 # exec(open(r'D:\programming\testingjs\fuckingKillHebrew\helpme.py').read())

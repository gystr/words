from django.db import models
import datetime
from django.utils import timezone
import json

# Create your models here.

class Word(models.Model):
    word_name = models.CharField(max_length=144)
    word_def = models.CharField(max_length=200)
    word_example = models.CharField(max_length=200,default=None)
    pub_date = models.DateTimeField('date published')
    # word_tag = models.CharField(max_length=100,default=None)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "{} - {}".format(self.word_name,self.word_def)

    # def set_tags(self, x):
    #     self.word_tag = json.dumps(x)
    #
    # def get_tags(self):
    #     return json.loads(self.word_tag)

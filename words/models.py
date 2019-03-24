from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User





class Tag(models.Model):
    tag_name = models.CharField(max_length=144,unique=True)
    tag_slug = models.CharField(max_length=144)
    tag_pub_date  = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False,name="is_main_field",null=False)


    def __str__(self):
        return "{}".format(self.tag_name)

    def __repr__(self):
        return "{}".format(self.tag_slug)

class Word(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    word_name = models.CharField(max_length=144)
    word_def = models.CharField(max_length=200)
    word_example = models.CharField(max_length=200,default=None)
    pub_date = models.DateTimeField('date published')
    word_tag = models.ManyToManyField(Tag)
    num_vote_up = models.IntegerField(default=0)
    num_vote_down = models.IntegerField(default=0)
    upvoted_by = models.CharField(max_length=1000,default="0,")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "{} - {}".format(self.word_name,self.word_def)

    def voted_by_this_user(self,user_pk):
        print(user_pk)
        if self.upvoted_by == "":
            return False
        x = self.upvoted_by.split(",")
        x_set = set(x)
        if str(user_pk) in x_set:
            return True
        else:
            return False

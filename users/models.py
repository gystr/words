from django.db import models
from django.contrib.auth.models import User
from words.models import Word
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    published_words = models.ManyToManyField(Word, related_name='user_published_words')
    voted_words = models.ManyToManyField(Word, related_name='user_voted_words')


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f"username:{self.user.username}  pk:{str(self.user.pk)}"


    def can_vote(self,word):
        """
        this function is called in words.views.vote() and checks if the user already
        voted on this word
        """
        if word in self.voted_words.all():
            return False
        else:
            return True

    def can_publish(self):
        """
        this function checks if the user didn't publish too many words today
        first checking if super user and if not did he publish more than 3 words in the last day
        if he is a superuser or is allowed to publish return True
        """
        if self.user.is_superuser:
            return True
        counter = 0
        for word in self.published_words.all():
            if word.was_published_recently():
                counter += 1

        if counter > 3:
            return False

        return True

from django import forms

class WordForm(forms.Form):
    word_name = forms.CharField(label='word_name', max_length=100)
    word_def = forms.CharField(label="word_def",max_length=200,widget=forms.Textarea)
    word_example = forms.CharField(label="word_example",max_length=200,widget=forms.Textarea)

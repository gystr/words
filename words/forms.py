from django import forms

class WordForm(forms.Form):
    word_name = forms.CharField(label='מילה', max_length=100)
    word_def = forms.CharField(label="הגדרה",max_length=200,widget=forms.Textarea)
    word_example = forms.CharField(label="דוגמא",max_length=200,widget=forms.Textarea)
    word_tags = forms.CharField(label='קטגוריות', max_length=100)

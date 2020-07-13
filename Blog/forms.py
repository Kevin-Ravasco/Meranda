from django.forms import ModelForm, Textarea, Form, TextInput
from django import forms
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'website', 'message', 'parent')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'website': TextInput(attrs={'class': 'form-control'}),
            'message': Textarea(attrs={'cols': 40, 'rows': 7, 'class': 'form-control'}),
            'parent': Textarea(attrs={'class': 'form-control', "type": "hidden"})
        }


class ContactForm(Form):
    first_name = forms.CharField(max_length=500, label="Name", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg'}))
    last_name = forms.CharField(max_length=500, label="Name", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(max_length=500, label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg'}))
    tel_number = forms.IntegerField(label="tel", widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-lg'}))
    message = forms.CharField(label='message', widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your comment here', 'class': 'form-control form-control-lg',
                               'cols': 30, 'rows': 10}))
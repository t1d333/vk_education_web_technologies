from django import forms
from app import models
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    username.widget.attrs['placeholder'] = 'Enter username'
    password.widget.attrs['placeholder'] = 'Enter password'


class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.Profile
        fields = ["username", "email", "password", "password_repeat", "avatar"]

    labels = {
        password_repeat: _('Repeat password')
    }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError(
                message="Username is too short",
                code="invalid_username")

        if len(models.Profile.objects.filter(username=username)):
            raise forms.ValidationError(
                message="User with the same name already exists",
                code="invalid_username")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if len(models.Profile.objects.filter(email=email)) > 0:
            raise forms.ValidationError(
                message="This email already registred",
                code="invalid_email")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        password_repead = cleaned_data["password_repeat"]
        if len(password) < 6:
            raise forms.ValidationError(
                message="Password is too short",
                code="invalid_password")
        if password and (password != password_repead):
            self.add_error('password', '')
            self.add_error('password_repeat', '')
            raise forms.ValidationError(
                message="Passwords do not match",
                code="invalid_password")

    def save(self):
        self.cleaned_data.pop('password_repeat')
        avatar = self.cleaned_data.pop('avatar')
        user = auth.models.User.objects.create_user(**self.cleaned_data)
        models.Profile.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            user=user,
            avatar=avatar)
        self.cleaned_data.pop('email')
        return self.cleaned_data


class QuestionForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = models.Question
        fields = ['title', 'text', 'tags']

    tags.widget.attrs['placeholder'] = 'Enter no more than three tags separated by commas'

    def clean_tags(self):

        tags_list = self.cleaned_data['tags'].split(', ')
        tags_set = set(tags_list)
        if len(tags_set) != len(tags_list):
            raise forms.ValidationError(
                message="Tags must not be the same",
                code="invalid_tags")

        if (0 == len(tags_set)) or (len(tags_set) > 3):
            raise forms.ValidationError(
                message="Tags count must be valid",
                code="invalid_tags")
        for tag in tags_list:
            if len(tag) > 15:
                raise forms.ValidationError(
                    message="Tag length must be less than 15")
        return self.cleaned_data['tags']

    def save(self, username):
        author = models.Profile.objects.get(username=username)
        tags = {
            models.Tag.objects.get_or_create(
                name=tag) for tag in set(
                self.cleaned_data.pop('tags').split(','))}
        question = models.Question.objects.create(
            author=author, **self.cleaned_data)
        for tag in tags:
            question.tags.add(tag[0])
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['text']
        labels = {
            'text': _(''),
        }

    def save(self, request: HttpRequest):
        author = models.Profile.objects.get(username=request.user.username)
        question = models.Question.objects.get(pk=request.path.split('/')[-1])
        return models.Answer.objects.create(
            author=author,
            question=question,
            **self.cleaned_data)

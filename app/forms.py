from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#class RegisterForm(forms.Form)


#class QuestionCreationForm(forms.Form):


#class AnswerCreationForm(forms.Form):

from django import forms
from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


from classroom.models import eUser, Category, Post, Comment, ClassList, Event, Class, files, Professor

class SignUpForm(UserCreationForm):
    student_num = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], required=True)
    name = forms.CharField(max_length=32, required=True)
    dept = forms.CharField(max_length=32, required=True)
    is_professor = forms.BooleanField()

    class Meta:
        model = eUser
        fields = ('student_num', 'name', 'dept', 'is_professor', 'password1', 'password2')

class LogInForm(forms.Form):
    student_num = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    password = forms.CharField(widget=forms.PasswordInput())

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'text' : forms.Textarea(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'class_id']

        widgets ={
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'class_id' : forms.Select(attrs={'class': 'form-control'}),

        }
class ClassAssignForm(forms.ModelForm):
    class Meta:
        model = ClassList
        fields = ['classes', ]

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'start_time' : DateTimeInput(attrs={'type': 'datatime-local'}, format='%Y-%m-%d%H:%M'),
            'end_time' : DateTimeInput(attrs={'type': 'datatime-local'}, format='%Y-%m-%d%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%d%H:%M', )
        self.fields['end_time'].input_formats = ('%Y-%m-%d%H:%M', )

class UploadForm(forms.ModelForm):
    class Meta:
        model = files
        fields = ['description', 'file', ]

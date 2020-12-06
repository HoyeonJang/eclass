from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm


from .models import eUser, Post, Class, Category, ClassList, Comment, Professor

# Register your models here.


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    class Meta:
        model = eUser
        fields = ('student_num', 'name', 'dept', 'is_professor', )

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = eUser
        fields = '__all__'

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('student_num', 'name', 'dept', 'is_admin', 'is_professor')
    list_filter = ('is_admin', 'is_professor')
    fieldsets = (
        (None, {'fields': ('student_num', 'password')}),
        ('Personal info', {'fields': ('name', 'dept', 'is_professor',)}),
        ('Permsissions', {'fields': ('is_admin',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('student_num', 'name', 'dept', 'is_professor', 'password1', 'password2'),
        }),
    )

    search_fields = ('student_num',)
    ordering = ('name',)
    filter_horizontal = ()


admin.site.register(eUser, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Class)
admin.site.register(ClassList)
admin.site.register(Professor)
admin.site.register(Comment)

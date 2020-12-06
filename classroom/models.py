from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, student_num, name, dept, is_professor, password=None):

        if not student_num:
            raise ValueError("Must have id")

        user = self.model(
            student_num=student_num,
            name=name,
            dept=dept,
            is_professor=is_professor
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, student_num, name, dept, is_professor, password=None):

        user = self.create_user(
            student_num=student_num,
            name=name,
            dept=dept,
            is_professor=is_professor,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)

        return user

class eUser(AbstractBaseUser):
    student_num = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], unique=True)
    name = models.CharField(max_length=32)
    dept = models.CharField(default='None', max_length=32)
    create_date = models.DateField(auto_now_add=True)
    is_professor = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'student_num'
    REQUIRED_FIELDS = ['name', 'dept', 'is_professor']

    def __str__(self):
        return self.name + "-" + self.student_num

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Professor(models.Model):
    user = models.OneToOneField(eUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class Class(models.Model):
    title = models.CharField(max_length=32, unique=True)
    season = models.CharField(max_length=32)
    start_time = models.TimeField(auto_now=False, blank=True)
    end_time = models.TimeField(auto_now=False, blank=True)
    students_num = models.IntegerField(default=0)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    students = models.ManyToManyField(eUser, through="ClassList")

    class Meta:
        ordering = ('-title', )

    @property
    def __str__(self):
        return self.title

class ClassList(models.Model):
    student = models.ForeignKey(eUser, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.classes.title + "-" + self.student.name

    def get_absolute_url(self):
        return reverse('classroom:index')

class Category(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, default="none")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom:index')

class Post(models.Model):
    author = models.ForeignKey(eUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=64)
    text = models.TextField(max_length=20000)
    created_date = models.DateTimeField(auto_now=True, editable=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    views = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ('-created_date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom:post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    author = models.ForeignKey(eUser, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.text

class Event(models.Model):
    title = models.CharField(max_length=32)
    desc = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_html_url(self):
        url = reverse('', args=(self.id, ))
        return f'<a href="{url}"> {self.title} </a>'

class files(models.Model):
    file = models.FileField()
    address = models.GenericIPAddressField(auto_created=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
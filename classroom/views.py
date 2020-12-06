from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic.edit import DeleteView, FormView, CreateView, UpdateView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import SignUpForm, LogInForm, PostForm, CategoryForm, UploadForm, ClassAssignForm
from .models import ClassList, eUser, Category, Class, Post, Comment, files, Professor

def home(request):
    return render(request, 'classroom/base.html')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('student_num')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = SignUpForm()
    return render(request, 'classroom/signup.html', {'form':form})

class LogInView(FormView):
    template_name = 'classroom/login.html'
    form_class = LogInForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('student_num')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(reverse('classroom:index'))
        return redirect('classroom:login')

def LogOut(request):
    logout(request)
    return redirect(reverse('classroom:home'))

class ClassListView(LoginRequiredMixin, ListView):
    model = ClassList
    template_name = 'classroom/index.html'
    context_object_name = 'classes'
    login_url = '/login/'

    def get_queryset(self):
        user = get_object_or_404(eUser, pk=self.request.user.pk)
        return self.model.objects.filter(student=user)

class CategoryView(ListView):
    model = Category
    template_name = 'classroom/lecture.html'
    context_object_name = 'categories'

    def get_queryset(self):
        class_pk = get_object_or_404(Class, pk=self.kwargs.get('pk'))
        return self.model.objects.filter(class_id=class_pk)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        post_list = Post.objects.all()
        class_pk = get_object_or_404(Class, pk=self.kwargs.get('pk'))
        context.update({'post_list': post_list, 'class_pk': class_pk})
        return context

class Student_num(ListView):
    model = Class
    template_name = 'classroom/student_num.html'
    context_object_name = 'students'

    def get_queryset(self):
        class_pk = get_object_or_404(Class, pk=self.kwargs.get('pk'))
        return ClassList.objects.filter(classes=class_pk)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        c_id = self.kwargs.get('pk')
        object = Category.objects.filter(class_id=c_id)
        context.update({'object': object})
        return context

def ClassCreate(request, *args, **kwargs):
    if request.method == 'POST':
        pro = Professor.objects.get(user=request.user.pk)
        title = request.POST.get('title')
        season = request.POST.get('season')
        start_time = request.POST.get('start')
        end_time = request.POST.get('end')
        a = Class(title=title, professor=pro, season=season, start_time=start_time, end_time=end_time)
        a.save()
        ClassList(classes=a, student=eUser.objects.get(id=request.user.pk)).save()
    else:
        return redirect('classroom:index')
    return redirect('classroom:index')


class PostListView(ListView):
    model = Post
    template_name = 'classroom/post.html'
    context_object_name = 'posts'
    ordering = ['-created_date']

    def get_queryset(self):
        cate_pk = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return self.model.objects.filter(category=cate_pk)

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comment_list = Comment.objects.filter(post=self.kwargs.get('pk'))
        context.update({'comment_list': comment_list, })
        return context

class ClassAssignView(LoginRequiredMixin, CreateView):
    model = ClassList
    form_class = ClassAssignForm
    fields = ['classes', ]
    template_name = 'classroom/class_form.html'

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/index/lecture/'

    def user_check(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def CommentForm(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = eUser.objects.get(id=request.user.pk)
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
    else:
        return redirect('classroom:post_detail', pk=pk)
    return redirect('classroom:post_detail', pk=pk)

def UploadView(request, id):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FIELS)
        if form.is_valid():
            form.save()
            return redirect('post')
    else:
        form = UploadForm()
    return render(request, 'classroom:index', {'form': form})
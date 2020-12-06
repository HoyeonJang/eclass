from django.urls import path
from django.conf.urls import url
import classroom.views as views
from django.contrib.auth import views as auth_views


app_name = "classroom"

urlpatterns = [
    path('', views.home, name='home'),
    #path('index/<int:c_pk>', views.get_pk, name='get_pk'),
    path('index/', views.ClassListView.as_view(), name='index'),
    path('index/assign', views.ClassAssignView.as_view(), name='assign'),
    path('index/lecture/<int:pk>', views.CategoryView.as_view(), name='lecture'),
    path('index/lecture/create', views.ClassCreate, name='class_create'),
    path('index/lecture/<int:pk>/students', views.Student_num.as_view(), name='lecture_students'),
    path('index/lecture/<int:pk>/create', views.CategoryCreateView.as_view(), name='category_create'),
    path('index/lecture/posts/<int:pk>', views.PostListView.as_view(), name='posts'),
    path('index/lecture/posts/<int:pk>update', views.PostUpdateView.as_view(), name='post_update'),
    path('index/lecture/posts/create', views.PostCreateView.as_view(), name='post_create'),
    path('index/lecture/posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('index/lecture/posts/detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('index/lecture/posts/detail/<int:pk>/comment', views.CommentForm, name='add_comment'),
    path('index/lecture/posts/new', views.PostCreateView.as_view(), name='post_create'),
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOut, name='logout'),
]
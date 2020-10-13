# *****************************************************************
# imports
# *****************************************************************
from django.shortcuts import render,redirect
from .models import Posts,Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout
from . import signals
from . forms import UserRegisterForm , UserUpdateForm , ProfileUpdateForm ,UpdatePost
from django.utils import timezone
from django.core.paginator import Paginator

# *****************************************************************
# BlogMainPage
# *****************************************************************
def index(request):
    post = Posts.objects.values().order_by('-date_posted')
    print(request.user)
    paginator = Paginator(post, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts={'posts':post ,'page_obj': page_obj}

    return render(request ,'index.html',posts)


# *****************************************************************
# RegisterPage
# *****************************************************************
# def register(request):
#     form = UserRegisterForm()
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             # add data to the database
            
#             user=form.cleaned_data.get('username')
#             messages.success(request, 'Account created for'+user)
#             form.save()
#     context = {'form': form}
#     return render(request, 'register.html',context)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('/login_page')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
# *****************************************************************
# LoginPage
# *****************************************************************

def login_page(request):
    return render(request,'login.html')

def login1(request):

    if request.method == "POST":
        username = request.POST.get('name1')
        password = request.POST.get('password1')
        nm=username
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                nm={'nm':nm}
                return redirect('/home')
            else:
                return redirect('/login_page')
        else:
                return redirect('/login_page')


# *****************************************************************
# UserHomePage
# *****************************************************************
@login_required(login_url='/register')
def home(request):
    nm=request.user
    posts = Posts.objects.filter(author = request.user).order_by('-date_posted')
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts={'page_obj': page_obj,'posts':posts,'nm':nm}
    return render(request,'home.html',posts)


# *****************************************************************
# Logout
# *****************************************************************
@login_required(login_url='/register')
def logout_page(request):
    logout(request)
    return redirect("/")

# *****************************************************************
# AddBlog
# *****************************************************************

@login_required(login_url='/register')
def add_post(request):
    if request.method=='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        post=Posts(title=title,content=content,author=author)
        post.save()
    return render(request,'addblog.html')

# *****************************************************************
# ViewBlogs
# *****************************************************************
def posts_view(request,myid):
    post = Posts.objects.filter(post_id=myid)
    print(post)
    return render(request, 'postview.html', {'post': post[0]})


# *****************************************************************
# UpdateBlog
# *****************************************************************
@login_required(login_url='/register')
def update_post(request,myid):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        u=Posts.objects.get(post_id=myid)
        print(u)
        u.title=title
        u.content=content
        u.date_posted=timezone.now()
        u.save()
        return redirect('/home')
    else:            
        post = Posts.objects.filter(post_id=myid)
        updateblog_form=UpdatePost()
    print(post[0])
    context={'updateblog_form':updateblog_form,'post':post[0]}
    return render(request,'update_post.html',context)


# *****************************************************************
# DeleteBlog
# *****************************************************************
@login_required(login_url='/register')
def delete_blog(request,myid):
    post = Posts.objects.filter(post_id=myid)
    print(post)
    post={'post':post[0]}
    
    return render(request,'delete.html',post)

@login_required(login_url='/register')
def delete_blogfinal(request,myid):
    if request.method =='POST':
        print(myid)
        Posts.objects.get(post_id=myid).delete()
    return redirect('/home')


# *****************************************************************
# Profile Display and Update
# *****************************************************************

@login_required(login_url='/register')
def profile(request):
    if request.method == 'POST':
        context={}
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES , instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Profile is Updated')
            return redirect('/profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()
    context = {'u_form': u_form, 'p_form': p_form}

    return render(request,'profile.html',context)

# *****************************************************************
# *****************************************************************

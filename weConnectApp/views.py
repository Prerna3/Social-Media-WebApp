from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mylogin')
    
    context = {'registerform': form}

    return render(request, 'register.html', context)

def myLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    
    context = {'loginform': form}

    return render(request, 'mylogin.html', context)

@login_required(login_url='mylogin')
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'home.html', context)


@login_required(login_url='mylogin')
def myLogout(request):
    auth.logout(request)
    return redirect('mylogin')


@login_required(login_url='mylogin')
def profile(request, user):
    profile_object = User.objects.get(username=user)
    profile = Profile.objects.get(user=profile_object)
    user = profile.user
    userposts = Post.objects.filter(user=user)
    numberOfPosts = len(userposts)
    
    user = profile.user

    

    context = {
        'user': user,
        'profile_object': profile_object,
        'profile': profile,
        'userposts' : userposts,
        'numberOfPosts': numberOfPosts,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='mylogin')
def createProfile(request):
    user = request.user
    profile_exists = Profile.objects.filter(user=user).exists()
    if not profile_exists:
        if request.method == 'POST':
            user = request.user
            name = request.POST['name']
            about = request.POST['about']
            profilepic = request.FILES['profilePic']
            DOB = request.POST['DOB']
            Profile.objects.create(user=user, name=name, about=about, profilePic=profilepic, DOB=DOB)
            return redirect(reverse('profile', kwargs={'user': user}))
        else:
            return render(request, 'createProfile.html')
    else:
        return redirect('profile', user=user)


@login_required(login_url='mylogin')
def editProfile(request, user):
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        if request.method == 'POST':
            name = request.POST['name']
            about = request.POST['about']
            profilePic = request.FILES.get('profilePic')
            DOB = request.POST['DOB']

            if name:
                profile.name = name
            if about:
                profile.about = about
            if profilePic:
                profile.profilePic = profilePic
            if DOB:
                profile.DOB = DOB

            profile.save()
            return redirect('profile', user=user)

        return render(request, 'editProfile.html', {'profile': profile})


@login_required(login_url='mylogin')
def addPost(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES['image']
        caption = request.POST['caption']
        Post.objects.create(user=user, image=image, caption=caption)
        return redirect('home')
    else:
        return render(request, 'addPost.html')
    

@login_required(login_url='mylogin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('home')
    

@login_required(login_url='mylogin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('profile', user=request.user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('profile', user=request.user)
    else:
        return redirect('home')

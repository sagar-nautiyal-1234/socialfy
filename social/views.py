from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Follow, Comment, Profile
from django import forms
from django.db.models import Q

# ---------------------------- #
# Profile Edit Form
# ---------------------------- #
class ProfileForm(forms.ModelForm):
    remove_pic = forms.BooleanField(required=False, label="Remove profile picture")

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data.get('remove_pic') and profile.profile_pic:
            profile.profile_pic.delete(save=False)
            profile.profile_pic = 'profile_pics/default.jpg'
        if commit:
            profile.save()
        return profile

# ---------------------------- #
# Home View
# ---------------------------- #
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'social/home.html', {'posts': posts})

# ---------------------------- #
# Create Post
# ---------------------------- #
@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        return redirect('home')
    return render(request, 'social/create_post.html')

# ---------------------------- #
# Delete Post
# ---------------------------- #
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('profile', username=request.user.username)

# ---------------------------- #
# Like / Unlike Post
# ---------------------------- #
@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# ---------------------------- #
# Signup View
# ---------------------------- #
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'social/signup.html', {'form': form})

# ---------------------------- #
# Profile View
# ---------------------------- #
@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = user_profile.post_set.all().order_by('-created_at')
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()
    is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    if request.method == 'POST' and request.user == user_profile:
        content = request.POST.get('content')
        if content:
            Post.objects.create(author=request.user, content=content)
            return redirect('profile', username=username)

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'social/profile.html', context)

# ---------------------------- #
# Follow / Unfollow
# ---------------------------- #
@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('profile', username=username)

    relation = Follow.objects.filter(follower=request.user, following=target_user)
    if relation.exists():
        relation.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    return redirect('profile', username=username)

# ---------------------------- #
# Edit Profile
# ---------------------------- #
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'social/edit_profile.html', {'form': form})

# ---------------------------- #
# Search Users
# ---------------------------- #
@login_required
def search_users(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = User.objects.filter(Q(username__icontains=query)).exclude(username=request.user.username)

    return render(request, 'social/search.html', {'results': results, 'query': query})

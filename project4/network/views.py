from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages

from .models import User, Post, Follow


def index(request):   
    if request.method == "POST":
        content = request.POST["content"]
        if content.strip():
            post = Post(user=request.user, content=content)
            post.save()
            return HttpResponseRedirect(reverse("index"))

    posts = Post.objects.all().order_by("-timestamp")
    # paginator = Paginator(posts, 10)  # 10 posts per page
    # page_number = request.GET.get("page", 1)
    # page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#  --------  >>>>>>  Adding the new functions

def all_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    print(posts)
    posts_json = Post.objects.all().values()
    print(posts_json)
    print(" ------------------- ")
    posts_serialize = [post.serialize() for post in posts]
    print(posts_serialize)
    print(" ------       --------       ----- ")
    users = User.objects.all()
    print(users)
    users_json = User.objects.all().values()
    print(users_json)
    # paginator = Paginator(posts, 10)  # 10 posts per page
    # page_number = request.GET.get("page", 1)
    # page_obj = paginator.get_page(page_number)

    return render(request, "network/all_posts.html", {
        "posts": posts
    })


    # return JsonResponse({
    #     "posts": [{
    #         "id": post.id,
    #         "content": post.content,
    #         "timestamp": post.timestamp,
    #         "user": post.user.username,
    #         "likes": post.like_count()
    #     } for post in page_obj.object_list],
    #     "has_next": page_obj.has_next(),
    #     "has_previous": page_obj.has_previous(),
    # })


def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all().order_by("-timestamp")
    is_following = request.user.is_authenticated and user.followers.filter(follower=request.user).exists()
    
    return JsonResponse({
        "username": user.username,
        "followers_count": user.followers.count(),
        "following_count": user.following.count(),
        "posts": [{
            "id": post.id,
            "content": post.content,
            "timestamp": post.timestamp,
            "likes": post.like_count()
        } for post in posts],
        "is_following": is_following
    })


@login_required
def follow_unfollow(request, username):
    user_to_follow = User.objects.get(username=username)
    if user_to_follow == request.user:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    follow_obj, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    if not created:
        follow_obj.delete()
        return JsonResponse({"message": "Unfollowed successfully."})
    return JsonResponse({"message": "Followed successfully."})


@login_required
def like_unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        return JsonResponse({"message": "Unliked successfully.", "like_count": post.like_count()})
    post.likes.add(request.user)
    return JsonResponse({"message": "Liked successfully.", "like_count": post.like_count()})

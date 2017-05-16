import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render, render_to_response
from user_profile.models import User, UserFollowers
from models import Tweet, HashTag
from mytweets import settings
from tweets import forms as tweets_form
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.


def index(request):
    if request.method == 'GET':
        return HttpResponse('I am called from a get Request')
    elif request.method == 'POST':
        return HttpResponse('I am called from a post Request')


class Index(View):
    def get(self, request):
        # user = User.objects.all()
        params = {}
        params["name"] = "DuoDuo"
        return render(request, 'index.html', params)
        # return HttpResponse('I am called from a get Request')

    def post(self, request):
        return HttpResponse('I am called from a post Request')


class Profile(View):
    def get(self, request, username):
        params = {}
        userProfile = User.objects.get(username=username)
        userFollower = UserFollowers.objects.get(user=userProfile)
        if userFollower.followers.filter(username=request.user.username).exists():
            params["following"] = True
        else:
            params["following"] = False
        form = tweets_form.TweetForm(initial={'country': 'Global'})
        search_form = tweets_form.SearchForm
        tweets = Tweet.objects.filter(user=userProfile).order_by('-create_date')
        pagniator = Paginator(tweets, 5)
        page = request.GET.get('page')
        try:
            tweets = pagniator.page(page)
        except PageNotAnInteger:
            tweets = pagniator.page(1)
        except EmptyPage:
            tweets = pagniator.page(pagniator.num_pages)

        params['tweets'] = tweets
        params['profile'] = userProfile
        params['form'] = form
        params['search'] = search_form
        params['paginator'] = pagniator
        return render(request, 'profile.html', params)

    def post(self, request, username):
        follow = request.POST['follow']
        user = User.objects.get(username=request.user.username)
        userProfile = User.objects.get(username=username)
        userFollower, status = UserFollowers.objects.get_or_create(user=userProfile)
        if follow == 'true':
            userFollower.followers.add(user)
        else:
            userFollower.followers.remove(user)
        return HttpResponse(json.dumps(""), content_type="application/json")


class PostTweet(View):
    def post(self, request, username):
        form = tweets_form.TweetForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweet(text=form.cleaned_data['text'],
                          user=user,
                          country=form.cleaned_data['country'])
            tweet.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word[0] == "#":
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
        return HttpResponseRedirect('/user/' + username)


class HashTagCloud(View):
    def get(self, request, hashtag):
        params = dict()
        hashtag = HashTag.objects.get(name=hashtag)
        params['tweets'] = hashtag.tweet
        return render(request, 'hashtag.html', params)


class Search(View):
    def get(self, request):
        form = tweets_form.SearchForm()
        params = dict()
        params['search'] = form
        return render(request, 'search.html', params)

    def post(self, request):
        form = tweets_form.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query)
            context = Context({'query': query, "tweets": tweets})
            return_str = render_to_string('partials/_tweet_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type="application/json")
        else:
            HttpResponseRedirect("/search")


class UserRedirect(View):
    def get(self, request):
        return HttpResponseRedirect('/user/' + request.user.username)

class MostFollowedUsers(View):
    def get(self, request):
        userFollowers = UserFollowers.objects.order_by('-count')[:10]
        params = dict()
        params['userFollowers'] = userFollowers
        return render(request, 'users.html', params)

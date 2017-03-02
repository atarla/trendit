import tweepy
import random
from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from twitterapp import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key,config.access_secret)

api = tweepy.API(auth)

trends_list = api.trends_place(config.us_trends)

trends_list_set = set([trend['name']
                     for trend in trends_list[0]['trends']])

trends_list_vol = set([trend['tweet_volume']
                     for trend in trends_list[0]['trends']])

# print(trends_list_set)
# print(trends_list)
# print(trends_list_vol)

list_trends = trends_list_set.intersection(trends_list_set)

#
def index(request):
    json_list = trends_list_set
    surprise_term = random.choice(list(json_list))
    # forums = Forum.objects.all()
    context = {'json_list':json_list,'surprise_term':surprise_term}
    return render(request, 'app/index.html', context)


def trend_results(request):
    if request.method=='GET':
            user_term = request.GET.get('searchterm')
            print(user_term)
            # user_term.save()
            trendresults = tweepy.Cursor(api.search, q=user_term).items(30)
            # forums = Forum.objects.all()
            results = set([i.text.encode("utf-8") for i in trendresults])
            context = {'user': request.user,'results':results,'searchterm':user_term}
            return render(request, 'app/results.html', context)




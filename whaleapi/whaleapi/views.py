from django.conf import settings
import requests
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.utils.html import escape


# sanitize form inputs
def cleaned_data(data):
    return escape(str(data))


callnumber=0
cachehit=0


# view function for get whales request
@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def getting(request):
    global callnumber, cachehit
    endpoint = 'https://whalemarket.saleswhale.io/whales'
    headers = {"Authorization": settings.BEARER_TOKEN}

    if request.method == 'GET':
        # increasing cache count
        callnumber += 1
        data = cleaned_data(request.GET.get('number'))
        if data:
            cached = cache.get(endpoint + "/" + data)
            # checking if cache data exists for current request
            if not cached:
                response = requests.get(endpoint + "/" + data, headers=headers)
                cache.set(endpoint + "/" + data, response)
            else:
                cachehit += 1
                response = cached
        else:
            cached = cache.get(endpoint)
            if not cached:
                response = requests.get(endpoint, headers=headers)
                cache.set(endpoint, response)
            else:
                cachehit += 1
                response = cached

        try:
            if response.json()["error"]:
                return render(request, "templates/none.html", {"id": data})
        except:
            return render(request, "templates/getrequest.html", {"results": response, "callnumber": callnumber, "cachehit": cachehit})


# view function for post whale request
@api_view(['GET', 'POST'])
@csrf_protect
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def posting(request):
    global callnumber, cachehit
    endpoint = 'https://whalemarket.saleswhale.io/whales/'
    headers = {"Authorization": settings.BEARER_TOKEN,
               "Content-Type": "application/json"}

    if request.method == 'POST':
        # get inputs from html page
        whalename = cleaned_data(request.POST.get('whaleName'))
        country = cleaned_data(request.POST.get('country'))
        # format API Post call
        whales = '{{"name": "{name}", "country": "{country}" }}'.format(name=whalename, country=country)
        response = requests.post(endpoint, whales, headers=headers)
        try:
            if response.json()["error"]:
                return render(request, "templates/none.html", {"whale": whales, "id": -999999})
        except:
            cache.delete(endpoint)
            return render(request, "templates/postrequest.html", {"results": response, "callnumber": callnumber, "cachehit": cachehit})


# return view for home page
def index(request):
    global callnumber, cachehit
    return render(request, "templates/home.html", {"cache": "false", "callnumber": callnumber, "cachehit": cachehit})


# view for clearing cache
def purgecache(request):
    global callnumber, cachehit
    cache.clear()
    callnumber = 0
    cachehit = 0
    return render(request, "templates/home.html", {"cache": "true", "callnumber": callnumber, "cachehit": cachehit})

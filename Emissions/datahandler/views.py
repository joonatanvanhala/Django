from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from collections import OrderedDict
from rest_framework.response import Response
import collections
import operator
import json
# Create your views here.

def index(request):
    url = "http://localhost:8000/api/emissions/"
    headers = {'Content-type': 'application/json'}
    payload = {
    	"country": "all",
    }
    global countries
    countries = requests.get(url, data=json.dumps(payload), headers=headers)
    content = {
      "countries" : json.dumps(json.loads(countries.text))
    }
     #return HttpResponse(records)
    return render(request, 'html/search.html', content)

def search(request):
    global rootEmissions
    if(request.method == 'POST'):
        country = request.POST['myCountry']
        url = "http://localhost:8000/api/emissions/"
        headers = {'Content-type': 'application/json'}
        #get data for country
        payload = {
        	"country": country,
        }
        countryRes = requests.get(url, data=json.dumps(payload), headers=headers)
        countryData = json.loads(countryRes.text)
        countryData = dict(collections.OrderedDict(sorted(countryData.items(), key=operator.itemgetter(0), reverse=True)))
        #get countries for search bar
        content = {
            "countryData": countryData,
            "countries" : json.dumps(json.loads(countries.text)),
            "selectedCountry" : country
        }
        return render(request, 'html/datatable.html', content)

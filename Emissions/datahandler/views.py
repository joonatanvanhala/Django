from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
from django.conf import settings
from urllib.request import urlopen
import requests
from datetime import datetime
from zipfile import ZipFile
from collections import OrderedDict
import zlib
import collections
import operator
from xml.etree import ElementTree
import sys, io
import zipfile

# Create your views here.
def index(request):
     global rootCountries
     urlCountries = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=xml"
     rootCountries = getXml(urlCountries)
     global countries
     countries = findCountries()
     content = {
      "countries" : countries
     }
     #return HttpResponse(records)
     return render(request, 'index/search.html', content)

def findCountries():
    countries = []
    for record in rootCountries.findall("data/record"):
        country = record.find("field/[@name = 'Country or Area']").text
        if len(countries) > 0 and country != countries[len(countries) - 1]:
            countries.append(country)
        elif len(countries) == 0:
            countries.append(country)
    return countries

def search(request):
    global rootEmissions
    if(request.method == 'POST'):
        country = request.POST['select']
        urlEmissions = "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=xml"
        rootEmissions = getXml(urlEmissions)
        countryEmissions = findCountrysEmissions(country)
        countryPopulation = findCountriesPopulation(country, request)
        percapita = emissionsPerCapita(countryPopulation, countryEmissions)
        content = {
            "emissions": percapita,
            "populations" : countryPopulation,
            "countries" : countries,
            "selectedCountry" : country 
        }
        return render(request, 'index/datatable.html', content)
    else:
        return redirect('/emissions')

def emissionsPerCapita(countryPopulation, countryEmissions):
        percapita = {} #key = country's emission value = per capita
        for year,emission in countryEmissions.items():
            if emission is None or countryPopulation.get(year) is None:
                strKey = "None" + year
                percapita[strKey] = "None"
            else:
                percapita[emission] = "{0:.6f}".format(float(emission) / float(countryPopulation.get(year)))
        return percapita

def findCountriesPopulation(country, request):
    populations = {}
    currentYear = datetime.now().year
    for record in rootCountries.findall("data/record"):
        if record.find("field/[@name = 'Country or Area']").text == country:
            year = record.find("field/[@name = 'Year']").text
            population = record.find("field/[@name = 'Value']").text
            populations[year] = population
            if year == str(currentYear - 2): #stop searching if last data year is reached
                sortedRecords = dict(collections.OrderedDict(sorted(populations.items(), key=operator.itemgetter(0), reverse=True)))
                return sortedRecords
    sortedRecords = dict(collections.OrderedDict(sorted(populations.items(), key=operator.itemgetter(0), reverse=True)))
    return sortedRecords

def findCountrysEmissions(country):
    records = {}
    currentYear = datetime.now().year
    for record in rootEmissions.findall("data/record"):
        if record.find("field/[@name = 'Country or Area']").text == country:
            year = record.find("field/[@name = 'Year']").text
            emissions = record.find("field/[@name = 'Value']").text
            records[year] = emissions
            if year == str(currentYear - 2): #stop searching if last data year is reached
                sortedRecords = dict(collections.OrderedDict(sorted(records.items(), key=operator.itemgetter(0), reverse=True)))
                return sortedRecords
    sortedRecords = dict(collections.OrderedDict(sorted(records.items(), key=operator.itemgetter(0), reverse=True)))
    return sortedRecords

def getXml(url):
     response = urlopen(url)
     data = response.read()
     myzipfile = zipfile.ZipFile(io.BytesIO(data))
     zipInfo = myzipfile.infolist()
     infoObj = zipInfo[0]
     str = myzipfile.read(infoObj.filename)
     root = ElementTree.fromstring(str)
     return root

from django.shortcuts import render, redirect
from django.http import HttpResponse
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
import json

# Create your views here.
def index(request):
     global rootCountries
     urlCountries = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=xml"
     rootCountries = getXml(urlCountries)
     global countries
     countries = findCountries()
     content = {
      "countries" : json.dumps(countries)
     }
     #return HttpResponse(records)
     return render(request, 'html/search.html', content)

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
        country = request.POST['myCountry']
        urlEmissions = "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=xml"
        rootEmissions = getXml(urlEmissions)
        emissions = getEmissions(country)
        countryData = getPopulation(emissions, country)
        countryData = dict(collections.OrderedDict(sorted(countryData.items(), key=operator.itemgetter(0), reverse=True)))
        content = {
            "countryData": countryData,
            "countries" : json.dumps(countries),
            "selectedCountry" : country
        }
        return render(request, 'html/datatable.html', content)
    else:
        return redirect('/emissions')


def getPopulation(countryData, country):
    populations = {}
    currentYear = datetime.now().year
    for record in rootCountries.findall("data/record"):
        if record.find("field/[@name = 'Country or Area']").text == country:
            year = record.find("field/[@name = 'Year']").text
            population = record.find("field/[@name = 'Value']").text
            if countryData[year][0] != "None" and population != None:
                percapita = "{0:.5f}".format(float(countryData[year][0]) / float(population))
                countryData[year].append(population)
                countryData[year].append(percapita)
            elif population != None:
                countryData[year].append(population)
                countryData[year].append("None")
            else:
                countryData[year].append("None")
                countryData[year].append("None")
            if year == str(currentYear - 2): #stop searching if last data year is reached
                return countryData
    return countryData

def getEmissions(country):
    records = {}
    currentYear = datetime.now().year
    for record in rootEmissions.findall("data/record"):
        if record.find("field/[@name = 'Country or Area']").text == country:
            year = record.find("field/[@name = 'Year']").text
            emissions = record.find("field/[@name = 'Value']").text
            if emissions != None:
                 records[year] = ["{0:.5f}".format(float(emissions))]
            else:
                 records[year] = ["None"]
            if year == str(currentYear - 2): #stop searching if last data year is reached
                return records
    return records

def getXml(url):
     response = urlopen(url)
     data = response.read()
     myzipfile = zipfile.ZipFile(io.BytesIO(data))
     zipInfo = myzipfile.infolist()
     infoObj = zipInfo[0]
     str = myzipfile.read(infoObj.filename)
     root = ElementTree.fromstring(str)
     return root

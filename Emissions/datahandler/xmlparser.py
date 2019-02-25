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

def xmlParser(json, rootCountries, rootEmissions):
    country = json["country"]
    #get request asks names of the countries
    if country == "all":
        countries = getCountries(rootCountries)
        return countries
    #get request asks all data from every country
    else:
        data = allData(country, rootCountries, rootEmissions)
        return data

def allData(country, rootCountries, rootEmissions):
    emissions = getEmissions(country, rootEmissions)
    countryData = getPopulation(emissions, country, rootCountries)
    return countryData

def getEmissions(country, rootEmissions):
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

def getPopulation(countryData, country, rootCountries):
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

def getCountries(rootCountries):
    countries = []
    for record in rootCountries.findall("data/record"):
        country = record.find("field/[@name = 'Country or Area']").text
        if len(countries) > 0 and country != countries[len(countries) - 1]:
            countries.append(country)
        elif len(countries) == 0:
            countries.append(country)
    return countries

def getXml(url):
     response = urlopen(url)
     data = response.read()
     myzipfile = zipfile.ZipFile(io.BytesIO(data))
     zipInfo = myzipfile.infolist()
     infoObj = zipInfo[0]
     str = myzipfile.read(infoObj.filename)
     root = ElementTree.fromstring(str)
     return root

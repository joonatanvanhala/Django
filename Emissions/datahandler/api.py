from rest_framework import viewsets, permissions
from django.shortcuts import render, redirect
from rest_framework import serializers, viewsets, routers, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .xmlparser import xmlParser, getXml



class emissionsAPIview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,  #allow only GET if not authenticated
    ]
    urlCountries = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=xml"
    urlEmissions = "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=xml"
    rootCountries = getXml(urlCountries)    #download xml file
    rootEmissions = getXml(urlEmissions)    #download xml file
    def get(self, request):
        json = request.data
        response = xmlParser(json, self.rootCountries, self.rootEmissions)
        return Response(response)

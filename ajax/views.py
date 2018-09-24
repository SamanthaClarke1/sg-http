# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import json

import shotgun_api3

# Create your views here.
def index(request):
	if "test" in request.GET:
		return HttpResponse(request.GET["test"])
	else:
		return HttpResponse("Please supply the test field")

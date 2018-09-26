# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import json
import os
import ast

import shotgun_api3

def connect():
	sg = shotgun_api3.Shotgun(os.getenv("SGURL"), login=os.getenv("SGUSER"), password=os.getenv("SGPASS"))
	return sg

sg = connect()

def needsParam(p):
	return JsonResponse(json.dumps({'err': 'Please specify a request with the '+str(p)+' parameter.', 'errcode': 400}))

def jsonResponse(resp):
	return HttpResponse(resp, content_type="application/json")

def parseStrList(str):
	list = ast.literal_eval(str)
	return list

acceptableRequests = [
	'find_one',
	'find',
	'delete'
]

# Create your views here.
def index(request):
	tfilters = None
	ttype = None
	treq = None
	if('filters' in request.GET):
		tfilters = parseStrList(request.GET['filters'])
	if('target' in request.GET):
		ttype = request.GET['type']
	if('id' in request.GET):
		tid = request.GET['id']
	if(not 'req' in request.GET):
		return needsParam('req')
	else:
		treq = request.GET['req']
		isAccepted = False
		for ar in acceptableRequests:
			if(treq == ar):
				isAccepted = True
				break
		if(not isAccepted):
			return jsonResponse(json.dumps({'err': 'Invalid request. Please choose from an acceptable request: '+str(acceptableRequests), 'errcode': 400}))
	
	if(treq == 'delete'):
		if(tid == None):
			return needsParam('id')
		if(treq == 'delete'):
			sg.delete(ttarget, tid)

	if(treq == 'find_one' or treq == 'find'):
		result = None
		if(ttype == None):
			return needsParam('target')
		if(tfilters == None):
			return needsParam('filters')
		if(treq == 'find_one'):
			print("\n\n\n")
			print(tfilters[0])
			print("\n\n\n")
			result = sg.find_one(ttype, tfilters)
		if(treq == 'find'):
			result = sg.find(ttype, tfilters)

		return jsonResponse(json.dumps({'err': '', 'errcode': 200, 'result': result}))
		

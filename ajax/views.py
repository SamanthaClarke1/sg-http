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
	return jsonResponse(json.dumps({'err': 'Please specify a request with the '+str(p)+' parameter.', 'errcode': 400}))

def jsonResponse(resp):
	return HttpResponse(resp, content_type="application/json")

def parseStrList(str):
	list = ast.literal_eval(str)
	return list

def str2bool(str):
	return str in ['true', 'True', '1']

acceptableRequests = [
	'find_one',
	'find',
	'delete',
	'revive',
	'readprefs',
	'readactivitystream',
	'textsearch',
	'update',
	'info',
	'summarize'
]

# Create your views here.
def index(request):
	result = None

	tfilters = None
	ttype = None
	treq = None
	tprefs = None
	tid = None
	ttext = None
	tprojids = None
	tlimit = None
	tentityTypes = None
	tfields = None
	torder = None
	tfilterOperator = None
	tpage = None
	tretiredonly = False
	tincludeArchived = True
	tadditionalPresets = None
	tdata = None
	tmeum = None
	tgrouping = None
	tsummaryFields = None

	if('retiredonly' in request.GET):
		tretiredonly = str2bool(request.GET['retiredonly'])
	if('includearchived' in request.GET):
		tincludeArchived = str2bool(request.GET['includearchived'])
	if('summaryfields' in request.GET):
		tsummaryFields = parseStrList(request.GET['summaryfields'])
	if('grouping' in request.GET):
		tgrouping = parseStrList(request.GET['grouping'])
	if('meum' in request.GET):
		tmeum = parseStrList(request.GET['meum'])
	if('data' in request.GET):
		tdata = parseStrList(request.GET['data'])
	if('additionalpresets' in request.GET):
		tadditionalPresets = parseStrList(request.GET['additionalpresets'])
	if('fields' in request.GET):
		tfields = parseStrList(request.GET['fields'])
	if('order' in request.GET):
		torder = parseStrList(request.GET['order'])
	if('filters' in request.GET):
		tfilters = parseStrList(request.GET['filters'])
	if('entitytypes' in request.GET):
		tentitytypes = parseStrList(request.GET['entitytypes'])
	if('filteroperator' in request.GET):
		tfilterOperator = request.GET['filteroperator']
	if('page' in request.GET):
		tpage = int(float(request.GET['page']))
	if('target' in request.GET):
		ttype = request.GET['type']
	if('id' in request.GET):
		tid = int(float(request.GET['id']))
	if('prefs' in request.GET):
		tprefs = request.GET['prefs']
	if('text' in request.GET):
		ttext = request.GET['text']
	if('projectids' in request.GET):
		tprojids = request.GET['projectids']
	if('limit' in request.GET):
		tlimit = int(float(request.GET['limit']))
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

	if(treq == 'info'):
		result = sg.info()

	if(treq == 'summarize'):
		if(ttype == None):
			return needsParam('type')
		if(tfilters == None):
			return needsParam('filters')
		if(tsummaryFields == None):
			return needsParam('summaryfields')
		result = sg.summarize(ttype, tfilters, tsummaryFields, tfilterOperator, tgrouping, tincludeArchived)
	
	if(treq == 'update'):
		if(ttype == None):
			return needsParam('type')
		if(tid == None):
			return needsParam('id')
		if(tdata == None):
			return needsParam('tdata')
		result = sg.update(ttype, tid, tdata, tmeum)

	if(treq == 'textsearch'):
		if(ttext == None):
			return needsParam('text')
		if(tentityTypes == None):
			return needsParam('entitytypes')
		result = sg.text_search(ttext, tentityTypes, tprojids, tlimit)

	if(treq == 'readprefs'):
		result = sg.preferences_read(tprefs)
	
	if(treq == 'delete' or treq == 'revive' or treq == 'readactivitystream' or treq == 'textsearch'):
		if(tid == None):
			return needsParam('id')
		if(treq == 'delete'):
			result = sg.delete(ttype, tid)
		if(treq == 'revive'):
			result = sg.revive(ttype, tid)
		if(treq == 'readactivitystream'):
			result = sg.activity_stream_read(ttype, tid)

	if(treq == 'find_one' or treq == 'find'):
		if(ttype == None):
			return needsParam('target')
		if(tfilters == None):
			return needsParam('filters')
		if(treq == 'find_one'):
			result = sg.find_one(ttype, tfilters, tfields, torder, tlimit, tfilterOperator, tretiredonly, tpage, tincludeArchived, tadditionalPresets)
		if(treq == 'find'):
			result = sg.find(ttype, tfilters, tfields, torder, tlimit, tfilterOperator, tretiredonly, tpage, tincludeArchived, tadditionalPresets)

	return jsonResponse(json.dumps({'err': '', 'errcode': 200, 'result': result}))
		

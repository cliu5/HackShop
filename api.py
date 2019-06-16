from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import urllib.request
import json
import ssl
def getResults(keywords ="shirt"):
    context = ssl._create_unverified_context()
    f =  urllib.request.urlopen('https://openapi.etsy.com/v2/listings/active?api_key=irz124oxaw6rq6n346nx99hk&keywords=' +keywords+ '&limit=3',context=context)
    d = f.read()#Reads f and stores Json inside d
    data = json.loads(d)
    results=data['results']
    return data

temp = getResults('Natural,foods,Fruit,Product,')
queryResults=temp['results']
context = ssl._create_unverified_context()
for i in queryResults:
    f =  urllib.request.urlopen('https://openapi.etsy.com/v2/listings/' + str(i['listing_id'])+ '/images/?api_key=irz124oxaw6rq6n346nx99hk',context=context)
    d = f.read()#Reads f and stores Json inside d
    data = json.loads(d)
    results=data['results']
    print(results[0]['url_75x75'])

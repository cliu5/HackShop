from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import urllib.request
import json
import ssl
def apii(keywords ="shirt"):
    context = ssl._create_unverified_context()
    f =  urllib.request.urlopen('https://openapi.etsy.com/v2/listings/active?api_key=irz124oxaw6rq6n346nx99hk&keywords=' +keywords+ '&limit=15',context=context)
    d = f.read()#Reads f and stores Json inside d
    data = json.loads(d)
    print(data)
apii('redshirt')

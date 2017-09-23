from django.shortcuts import  render
from pymongo import MongoClient
import pprint
from operator import itemgetter, attrgetter, methodcaller
from clouds.Cloud import Cloud
from django.http import HttpResponseRedirect
import random
import cloudinary
import cloudinary.uploader
import cloudinary.api

MAIN_CONNSTR = "mongodb://admin:121314qw@ds036617.mlab.com:36617/maindb"
MAIN_DB = "maindb"

def cloud(request):
    client = MongoClient(MAIN_CONNSTR)
    db = client[MAIN_DB]
    command = db.command("dbStats")
    col = db['Cloud']
    doc = col.find()
    cld = []
    for e in doc:
        cldName = e["Cloud_name"]
        key = e["Key"]
        sectet = e["Secret"]

        cloudinary.config(
            cloud_name=cldName,
            api_key=key,
            api_secret=sectet
        )

        total = 0.0
        try:
            uploads = cloudinary.api.resources(type="upload")['resources']
            for o in uploads:
                total = total + o['bytes']
            total = total / (1 << 20)
        except:
            total = -1

        cld.append((e["_id"], e["Cloud_name"], e["Key"], e["Secret"], round(total, 2)))# str(stats) + " MB"
    cld = sorted(cld, key=itemgetter(1), reverse=True)
    return render(request, 'cloud.html', locals())

def generateId(LEN = 16):
    _id = "";
    for i in range(0, LEN):
        e = random.randrange(0, 100000)
        val = random.randrange(0, 26)
        if e & 1:
            _id = _id + chr(ord('a') + val)
        else:
            _id = _id + chr(ord('A') + val)
    return _id

def save_cloud(request):
    if request.method == 'POST':
        id = request.POST['_id']
        cloudName = request.POST['cloudName']
        key = request.POST['key']
        secret = request.POST['secret']
        if (not cloudName) or (not key) or (not secret):
            return HttpResponseRedirect('/cloud/error')
        if not id:
            id = generateId()
        clsaver = Cloud(MAIN_CONNSTR, MAIN_DB)
        clsaver.fill(id, cloudName, key, secret)
        clsaver.save(clsaver)
    return HttpResponseRedirect('/cloud/')

def drop_cloud(request):
    if request.method == 'POST':
        id = request.POST['_id']
        if id:
            clremover = Cloud(MAIN_CONNSTR, MAIN_DB)
            clremover.fill(id)
            clremover.remove(clremover)
        else:
            return HttpResponseRedirect('/cloud/error')
    return HttpResponseRedirect('/cloud/')

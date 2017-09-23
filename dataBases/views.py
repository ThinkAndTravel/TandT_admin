from django.shortcuts import  render
from pymongo import MongoClient
import pprint
from operator import itemgetter, attrgetter, methodcaller
from dataBases.DataBase import DataBase
from django.http import HttpResponseRedirect
import random

MAIN_CONNSTR = "mongodb://admin:121314qw@ds036617.mlab.com:36617/maindb"
MAIN_DB = "maindb"

def db(request):
    client = MongoClient(MAIN_CONNSTR)
    mess = "Allo"
    db = client[MAIN_DB]
    command = db.command("dbStats")
    col = db['DB']
    doc = col.find()
    s = ""
    dbs = []
    for e in doc:
        conn_str = str(e["ConnectingString"])
        db_name = str(e["dbName"])
        client2 = MongoClient(conn_str)
        db2 = client2[db_name]
        stats = ""
        try:
            comm = db2.command("dbStats")
            #size = dataSize + indexSize
            stats = round((float(comm['dataSize']) + float(comm['indexSize'])) / (1 << 20), 2)
        except:
            stats = -1
        dbs.append((e["_id"], e["dbName"], e["ConnectingString"], e["CollectionName"],stats))# str(stats) + " MB"
    dbs = sorted(dbs, key=itemgetter(1), reverse=True)
    return render(request, 'db.html', locals())

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



def save_db(request):
    if request.method == 'POST':
        id = request.POST['_id']
        dbName = request.POST['dbName']
        connectionString = request.POST['connectionString']
        dataType = request.POST['dataType']
        if (not dbName) or (not connectionString) or (not dataType):
            return HttpResponseRedirect('/db/error')
        if not id:
            id = generateId()
        dbsaver = DataBase(MAIN_CONNSTR, MAIN_DB)
        dbsaver.fill(id, dbName, connectionString, dataType)
        dbsaver.save(dbsaver)
        print(id, dbName, connectionString, dataType)
     #   db = DataBase(MAIN_CONNSTR, MAIN_DB)
    return HttpResponseRedirect('/db/')

def drop_db(request):
    if request.method == 'POST':
        id = request.POST['_id']
        if id:
            dbremover = DataBase(MAIN_CONNSTR, MAIN_DB)
            dbremover.fill(id)
            dbremover.remove(dbremover)
        else:
            return HttpResponseRedirect('/db/error')
    return HttpResponseRedirect('/db/')

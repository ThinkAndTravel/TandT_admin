from django.shortcuts import  render
from pymongo import MongoClient
import pprint
from operator import itemgetter, attrgetter, methodcaller
from dataBases.DataBase import DataBase


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
            stats = "Some fuck goes wrong with this db."
        dbs.append((e["_id"], e["dbName"], e["ConnectingString"], e["CollectionName"], str(stats) + " MB"))
    dbs = sorted(dbs, key=itemgetter(2), reverse=True)
    return render(request, 'index.html', locals())
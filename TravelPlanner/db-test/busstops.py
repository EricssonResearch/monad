# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
import bson
from bson.objectid import ObjectId

SERVER = False

client = MongoClient()
db = client.monad

def writeToDB():
    print('Do you really want to change the BusStop collection on ' + str(client) + '? ')
    sys.stdin.read(1)
    db.BusStop.insert_many(line1)
    db.BusStop.insert_many(line2)
    db.BusStop.insert_many(line3)
    db.BusStop.insert_many(line5)
    db.BusStop.insert_many(line14)
    return

line2 = [
{
    "_id" : ObjectId("562a07c473b23914826f046f"),
    "latitude" : 59.8974234000000010,
    "name" : "Kungshögarna",
    "longitude" : 17.6352009999999986
},
{
    "_id" : ObjectId("562a07c473b23914826f0470"),
    "latitude" : 59.8937918000000025,
    "name" : "Regins väg",
    "longitude" : 17.6396699999999989
},
{
    "_id" : ObjectId("562a07c473b23914826f0471"),
    "latitude" : 59.8936453999999969,
    "name" : "Valhalls väg",
    "longitude" : 17.6447512000000017
},
{
    "_id" : ObjectId("562a07c473b23914826f0472"),
    "latitude" : 59.8933053000000015,
    "name" : "Huges väg",
    "longitude" : 17.6495062000000011
},
{
    "_id" : ObjectId("562a07c473b23914826f0473"),
    "latitude" : 59.8882134999999991,
    "name" : "Topeliusgatan",
    "longitude" : 17.6487985999999992
},
{
    "_id" : ObjectId("562a07c473b23914826f0474"),
    "latitude" : 59.8865786000000000,
    "name" : "Värnlundsgatan",
    "longitude" : 17.6454076999999998
},
{
    "_id" : ObjectId("562a07c473b23914826f0475"),
    "latitude" : 59.8810458000000025,
    "name" : "Ferlinsgatan",
    "longitude" : 17.6491949999999989
},
{
    "_id" : ObjectId("562a07c473b23914826f0476"),
    "latitude" : 59.8774537999999978,
    "name" : "Heidenstamstorg",
    "longitude" : 17.6455243000000017
},
{
    "_id" : ObjectId("562a07c473b23914826f0477"),
    "latitude" : 59.8745814999999979,
    "name" : "Kantorsgatan",
    "longitude" : 17.6443329999999996
},
{
    "_id" : ObjectId("562a07c473b23914826f0478"),
    "latitude" : 59.8680372999999975,
    "name" : "Djäknegatan",
    "longitude" : 17.6395483000000013
},
{
    "_id" : ObjectId("562a07c473b23914826f0479"),
    "latitude" : 59.8683432999999994,
    "name" : "Portalgatan",
    "longitude" : 17.6374992000000006
},
{
    "_id" : ObjectId("562a07c473b23914826f047a"),
    "latitude" : 59.8647132999999982,
    "name" : "Höganäsgatan",
    "longitude" : 17.6405612000000005
},
{
    "_id" : ObjectId("562a07c473b23914826f047b"),
    "latitude" : 59.8618896999999990,
    "name" : "Väderkvarnsgatan",
    "longitude" : 17.6479104000000007
},
{
    "_id" : ObjectId("562a07c473b23914826f047c"),
    "latitude" : 59.8614214500000017,
    "name" : "Vaksala torg",
    "longitude" : 17.6470993259306006
},
{
    "_id" : ObjectId("562a07c473b23914826f047d"),
    "latitude" : 59.8604316999999995,
    "name" : "Stadshuset",
    "longitude" : 17.6404846999999982
},
{
    "_id" : ObjectId("562a07c473b23914826f047e"),
    "latitude" : 59.8591772999999989,
    "name" : "Skolgatan",
    "longitude" : 17.6254670000000004
},
{
    "_id" : ObjectId("562a07c473b23914826f047f"),
    "latitude" : 59.8650401000000016,
    "name" : "Götgatan",
    "longitude" : 17.6250932999999996
},
{
    "_id" : ObjectId("562a07c473b23914826f0480"),
    "latitude" : 59.8594141499999992,
    "name" : "Ekonomikum",
    "longitude" : 17.6197556556357995
},
{
    "_id" : ObjectId("562a07c473b23914826f0481"),
    "latitude" : 59.8576671000000005,
    "name" : "Studentstaden",
    "longitude" : 17.6131366999999983
},
{
    "_id" : ObjectId("562a07c473b23914826f0482"),
    "latitude" : 59.8559593000000021,
    "name" : "Rickomberga",
    "longitude" : 17.6031045000000006
},
{
    "_id" : ObjectId("562a07c473b23914826f0483"),
    "latitude" : 59.8520865999999998,
    "name" : "Oslogatan",
    "longitude" : 17.6049280000000010
},
{
    "_id" : ObjectId("562a07c473b23914826f0484"),
    "latitude" : 59.8497643999999980,
    "name" : "Reykjaviksgatan",
    "longitude" : 17.6019605000000006
},
{
    "_id" : ObjectId("562a07c473b23914826f0485"),
    "latitude" : 59.8507176000000030,
    "name" : "Ekebyhus",
    "longitude" : 17.5982623999999994
},
{
    "_id" : ObjectId("562a07c473b23914826f0486"),
    "latitude" : 59.8502183000000016,
    "name" : "Sernanders väg",
    "longitude" : 17.5921205000000000
},
{
    "_id" : ObjectId("562a07c473b23914826f0487"),
    "latitude" : 59.8525519000000017,
    "name" : "Flogsta centrum",
    "longitude" : 17.5876978000000008
},
{
    "_id" : ObjectId("562a07c473b23914826f0488"),
    "latitude" : 59.8509103999999965,
    "name" : "Flogsta vårdcentral",
    "longitude" : 17.5833831352062013
},
{
    "_id" : ObjectId("562a07c473b23914826f0489"),
    "latitude" : 59.8471839999999986,
    "name" : "Ihres väg",
    "longitude" : 17.5863857000000010
},
{
    "_id" : ObjectId("562a07c473b23914826f048a"),
    "latitude" : 59.8473206999999974,
    "name" : "Noreens väg",
    "longitude" : 17.5925501000000004
},
{
    "_id" : ObjectId("562a07c473b23914826f048b"),
    "latitude" : 59.8470549999999974,
    "name" : "Säves väg",
    "longitude" : 17.5959901999999992
}]

line14 = [
{
    "_id" : ObjectId("56321850aef06e102712207f"),
    "latitude" : 59.888051,
    "name" : "Garnisonen",
    "longitude" : 17.607451
},
{
    "_id" : ObjectId("56321850aef06e1027122080"),
    "latitude" : 59.885454,
    "name" : "Bärbygatan",
    "longitude" : 17.618129
},
{
    "_id" : ObjectId("56321850aef06e1027122081"),
    "latitude" : 59.884512,
    "name" : "Bärbyparken",
    "longitude" : 17.614932
},
{
    "_id" : ObjectId("56321850aef06e1027122082"),
    "latitude" : 59.883483,
    "name" : "Flottiljgatan",
    "longitude" : 17.609353
},
{
    "_id" : ObjectId("56321850aef06e1027122083"),
    "latitude" : 59.881960,
    "name" : "Flottörgatan",
    "longitude" : 17.612894
},
{
    "_id" : ObjectId("56321850aef06e102712209b"),
    "latitude" : 59.880836,
    "name" : "Flygargatan",
    "longitude" : 17.615216
},
{
    "_id" : ObjectId("56321850aef06e1027122084"),
    "latitude" : 59.880264,
    "name" : "Startgatan",
    "longitude" : 17.614675
},
{
    "_id" : ObjectId("56321850aef06e1027122085"),
    "latitude" : 59.878649,
    "name" : "Fjärdhundragatan",
    "longitude" : 17.617968
},
{
    "_id" : ObjectId("56321850aef06e1027122086"),
    "latitude" : 59.876501,
    "name" : "Väpnargatan",
    "longitude" : 17.618805
},
{
    "_id" : ObjectId("56321850aef06e1027122087"),
    "latitude" : 59.874531,
    "name" : "Torbjörnsgatan",
    "longitude" : 17.621688
},
{
    "_id" : ObjectId("56321850aef06e1027122088"),
    "latitude" : 59.873287,
    "name" : "Sköldungagatan",
    "longitude" : 17.625703
},
{
    "_id" : ObjectId("56321850aef06e1027122089"),
    "latitude" : 59.872496,
    "name" : "Idrottsgatan",
    "longitude" : 17.624909
},
{
    "_id" : ObjectId("56321850aef06e102712208a"),
    "latitude" : 59.870950,
    "name" : "Fyrishov entre",
    "longitude" : 17.623578
},
{
    "_id" : ObjectId("56321850aef06e102712208b"),
    "latitude" : 59.869216,
    "name" : "Svartbäckens vårdcentral",
    "longitude" : 17.627945
},
{
    "_id" : ObjectId("56321850aef06e102712208c"),
    "latitude" : 59.866600,
    "name" : "Polishuset",
    "longitude" : 17.629427
},
{
    "_id" : ObjectId("56321850aef06e102712208d"),
    "latitude" : 59.858401,
    "name" : "Centralstationen",
    "longitude" : 17.645222
},
{
    "_id" : ObjectId("56321850aef06e102712208e"),
    "latitude" : 59.856072,
    "name" : "Bäverns gränd",
    "longitude" : 17.644951
},
{
    "_id" : ObjectId("56321850aef06e102712208f"),
    "latitude" : 59.853480,
    "name" : "Svandammen",
    "longitude" : 17.639201
},
{
    "_id" : ObjectId("56321850aef06e1027122090"),
    "latitude" : 59.850043,
    "name" : "Akademiska sjukhuset",
    "longitude" : 17.643296
},
{
    "_id" : ObjectId("56321850aef06e1027122091"),
    "latitude" : 59.846250,
    "name" : "Akademiska sjukhuset södra",
    "longitude" : 17.637455
},
{
    "_id" : ObjectId("56321850aef06e1027122092"),
    "latitude" : 59.843357,
    "name" : "Uppsala Science Park",
    "longitude" : 17.638316
},
{
    "_id" : ObjectId("56321850aef06e1027122093"),
    "latitude" : 59.839808,
    "name" : "Grindstugan",
    "longitude" : 17.639811
},
{
    "_id" : ObjectId("56321850aef06e1027122094"),
    "latitude" : 59.832502,
    "name" : "Rosendals skola",
    "longitude" : 17.639644
},
{
    "_id" : ObjectId("56321850aef06e1027122095"),
    "latitude" : 59.826607,
    "name" : "Tallbäcksvägen",
    "longitude" : 17.629726
},
{
    "_id" : ObjectId("56321850aef06e1027122096"),
    "latitude" : 59.822601,
    "name" : "Fältvägen",
    "longitude" : 17.626049
},
{
    "_id" : ObjectId("56321850aef06e1027122097"),
    "latitude" : 59.821406,
    "name" : "Valsätraskolan",
    "longitude" : 17.628920
},
{
    "_id" : ObjectId("56321850aef06e1027122098"),
    "latitude" : 59.818191,
    "name" : "Barkspadevägen",
    "longitude" : 17.633466
},
{
    "_id" : ObjectId("56321850aef06e1027122099"),
    "latitude" : 59.813201,
    "name" : "Linrepevägen",
    "longitude" : 17.634851
},
{
    "_id" : ObjectId("56321850aef06e102712209a"),
    "latitude" : 59.811230,
    "name" : "Gottsunda Centrum",
    "longitude" : 17.627448
}]

line1 = [
{
    "_id" : ObjectId("5640a09273b239624322ed1e"),
    "latitude" : 59.8407237999999992,
    "name" : "Polacksbacken",
    "longitude" : 17.6467722999999985
},
{
    "_id" : ObjectId("5640a09273b239624322ed1f"),
    "latitude" : 59.8382120999999998,
    "name" : "Lundellska skolan",
    "longitude" : 17.6507602000000006
},
{
    "_id" : ObjectId("5640a09273b239624322ed20"),
    "latitude" : 59.8357129999999984,
    "name" : "Uppsala Folkhögskola",
    "longitude" : 17.6496589999999998
},
{
    "_id" : ObjectId("5640a09273b239624322ed21"),
    "latitude" : 59.8328877000000006,
    "name" : "Emmy Rappes väg",
    "longitude" : 17.6465212999999999
},
{
    "_id" : ObjectId("5640a09273b239624322ed22"),
    "latitude" : 59.8309939000000028,
    "name" : "Gustaf Kjellbergs väg",
    "longitude" : 17.6527898999999984
},
{
    "_id" : ObjectId("5640a09273b239624322ed23"),
    "latitude" : 59.8280251500000020,
    "name" : "Kronparksgården",
    "longitude" : 17.6508467160190001
},
{
    "_id" : ObjectId("5640a09273b239624322ed24"),
    "latitude" : 59.827082,
    "name" : "Ekudden",
    "longitude" : 17.654046
},
{
    "_id" : ObjectId("5640a09273b239624322ed25"),
    "latitude" : 59.8180886000000029,
    "name" : "Veterinärvägen",
    "longitude" : 17.6478627999999986
},
{
    "_id" : ObjectId("5640a09273b239624322ed26"),
    "latitude" : 59.8156478000000007,
    "name" : "Campus Ultuna",
    "longitude" : 17.6591887999999990
},
{
    "_id" : ObjectId("5640a09273b239624322ed27"),
    "latitude" : 59.815486,
    "name" : "Djursjukhuset",
    "longitude" : 17.659307
},
{
    "_id" : ObjectId("5640a09273b239624322ed28"),
    "latitude" : 59.8139099999999999,
    "name" : "Arrheniusplan",
    "longitude" : 17.6670929000000001
}]

line3 = [
{
    "_id" : ObjectId("5641aa72aef06e0b819e352d"),
    "latitude" : 59.886610,
    "name" : "Östra Nyby",
    "longitude" : 17.655274
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e352e"),
    "latitude" : 59.880829,
    "name" : "Lagerlöfsgatan",
    "longitude" : 17.655277
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e352f"),
    "latitude" : 59.877178,
    "name" : "Almqvistgatan",
    "longitude" : 17.655591
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3530"),
    "latitude" : 59.873735,
    "name" : "Levertinsgatan",
    "longitude" : 17.653217
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3531"),
    "latitude" : 59.871273,
    "name" : "Wennerbergsgatan",
    "longitude" : 17.649222
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3532"),
    "latitude" : 59.866827,
    "name" : "Kvarntorget",
    "longitude" : 17.646846
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3533"),
    "latitude" : 59.822709,
    "name" : "Slädvägen",
    "longitude" : 17.625835
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3534"),
    "latitude" : 59.818918,
    "name" : "Spinnrocksvägen",
    "longitude" : 17.621812
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3535"),
    "latitude" : 59.813453,
    "name" : "Bandstolsvägen",
    "longitude" : 17.622348
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3536"),
    "latitude" : 59.809903,
    "name" : "Bröderna Berwalds väg",
    "longitude" : 17.624977
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3537"),
    "latitude" : 59.806952,
    "name" : "Vackra Birgers väg",
    "longitude" : 17.624846
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3538"),
    "latitude" : 59.804514,
    "name" : "Jenny Linds väg",
    "longitude" : 17.628342
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e3539"),
    "latitude" : 59.802935,
    "name" : "Solistvägen",
    "longitude" : 17.628674
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e353a"),
    "latitude" : 59.803692,
    "name" : "Flöjtvägen",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("5641aa72aef06e0b819e353b"),
    "latitude" : 59.805470,
    "name" : "Cellovägen",
    "longitude" : 17.637618
}]

line5 = [
{
    "_id" : ObjectId("568bdb7daef06e0dab282d2a"),
    "latitude" : 59.803692,
    "name" : "Stenhagenskolan",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d2b"),
    "latitude" : 59.803692,
    "name" : "Herrhagens Byväg",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d2c"),
    "latitude" : 59.803692,
    "name" : "Kiselvägen",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d2d"),
    "latitude" : 59.803692,
    "name" : "Stenhagens Centrum",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d2e"),
    "latitude" : 59.803692,
    "name" : "Stenröset",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d2f"),
    "latitude" : 59.803692,
    "name" : "Stenhällen",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d3a"),
    "latitude" : 59.803692,
    "name" : "Gatstenen",
    "longitude" : 17.632272
},
{
    "_id" : ObjectId("568bdb7daef06e0dab282d3b"),
    "latitude" : 59.803692,
    "name" : "Hedensbergsvägen",
    "longitude" : 17.632272
}]

writeToDB()

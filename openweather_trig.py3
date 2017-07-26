#!/usr/bin/python3
# -*- coding: utf8 -*-
# registers create alters and delets triggers and alerts by openweatermap.org
#   2017-23.07. Christoph Schultz

import urllib3, json, sys, pprint, argparse, datetime

def mkdate(datestr):
    try:
      return datetime.datetime.strptime(datestr, '%d.%m.%Y %H:%M')
    except ValueError:
      raise argparse.ArgumentTypeError(datestr + ' is not a proper date string')

pool = urllib3.PoolManager()
ow_appid ="1f422f257ebc8ab249c166e634260f9d"
ow_lat = 52
ow_long = 10
ow_url  = "http://api.openweathermap.org/data/3.0/triggers?appid=" + ow_appid
parser = argparse.ArgumentParser(description=' trigger tool for openweatermap by Christoph Schultz')
parser.add_argument('action')
args = parser.parse_args()
if args.action == "register":
   name = input("Trigger Ereignis:(temp,wind_speed,wind_dir, humidity, pressure, clouds)")
   begin = eval input("Beginn:[vor|in,x ](Tagen)"))
   end = eval (input("Ende: [vor|in,x] (Tagen) Ende > Beginn"))
   if begin[0] == "vor":
      start_exp = "before"
   else:
      start_exp = "after"
   
   if end [0]== "vor":
      end_exp = "before"
   else:
      end_exp = "after"
        
   
   trig_start = begin[1]*24*60*60
   trig_end = end[1]*24*60*60
   #print(trig_start, trig_end)
   ow_post_data = { 'time_period':{'start':{'expression':start_exp, 'amount': trig_start },'end':{'expression':end_exp,'amount':  trig_end }},'conditions':[{'name': name,'expression':'$gt','amount': 70}],
   'area':[{'type':'Point','coordinates':[ 52 ,  10 ]}]}
   print(ow_post_data)
   print(json.dumps(ow_post_data).encode('utf-8'))
   req = pool.request("POST", ow_url, body=json.dumps(ow_post_data).encode('utf-8'), headers={ 'Content-type': 'application/json'})
   res = req.data
   print(res)
 #---------------------------------------------------------------------
elif args.action == "alter":
   id = input("trigger_id:")
   c = input(" Wieviele Alarme? (max 2)")
   begin= eval([input("Beginn: [vor|in,x]Tagen")
   end = eval (input("Ende: [vor|in,x] (Tagen) Ende > Beginn"))
   i = 0
   while (i<c+1):
     trig[i] = eval(input("[name(str), Bedingung(grosser,kleiner,gleich), Wert(int)")
     name[i] = trig[i][0]	
     cond[i] = trig[i][1]
     val[i]  = trig[i][2]	
   if begin[0] == "vor":
      start_exp = "before"
   else:
      start_exp = "after"
   
   if end [0]== "vor":
      end_exp = "before"
   else:
      end_exp = "after"	 
   trig_start = begin[1]*24*3600
   trig_end = end[1]+24+3600
   ow_put_url = "http://api.openweathermap.org/data/3.0/triggers/" + id + "&appid=" + ow_appid
   ow_put_data = {'time_period':{'start':{'expression':start_exp, 'amount':trig_start}, 'end':{'expression':end_exp, 'amount':trig_end}},'contitions'[{'name': name[0], 'expression':'$gt', 'amount':amnt[0]},{'name':name[1],'expression':'$gt','amount':amnt[1]} ],
   'area':[{'type': 'Point','coordinates':[lat,lon]}]}
   
   req = pool.request("PUT", t_url, body=json.dumps(t_data).encode('utf-8'), headers={Content-type: 'application/json'})
   res=req.data
   print(res)
   
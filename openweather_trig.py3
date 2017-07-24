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
parser.add_argument('id', default=False)
parser.add_argument('start')
parser.add_argument('end')

args = parser.parse_args()
t_start = args.start
t_end = args.end
if args.action == "register":
   
   trig_start = 604800
   trig_end = 640800
   #print(trig_start, trig_end)
   ow_post_data = { 'time_period':{'start':{'expression':'before', 'amount': trig_start },'end':{'expression':'after','amount':  trig_end }},'condition':[{'name': 'wind_speed','expression':'$gt','amount': 70}],
   'area':[{'type':'Point','coordinates':[ 52 ,  10 ]}]}
   print(ow_post_data)
   print(json.dumps(ow_post_data).encode('utf-8'))
   req = pool.request("POST", ow_url, body=json.dumps(ow_post_data).encode('utf-8'), headers={ 'Content-type': 'application/json'})
   res = req.data
   
   print(res)
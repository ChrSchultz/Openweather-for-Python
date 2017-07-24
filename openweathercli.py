#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# client for openweather API
# - call PAI
# - translate fields if required
# - save JSON format in a file
# add this programm to crontab: crontab -e
# examle below will be excecuted every 15 minutes
# */15 * * * * python /home/pi/433/openweather_client.py Berlin > crontab_ow_client.log 2>&1
 
# 2013-06-23 V0.1 by Thomas Hoeser
#
 
import urllib2, json, sys, pprint, argparse
 
verbose_level = 0
debug_level = 0
 
#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
 
   pp = pprint.PrettyPrinter(indent=4)
 
   parser = argparse.ArgumentParser(description='open weather client by Thomas Hoeser / 2013')
   parser.add_argument("-v", "--verbose", default=False,
                          dest='verbose', help="increase output verbosity", type=int)
   parser.add_argument("-d", "--debug", action='store_const', dest='debug',
                    const='value-to-store', help="debug mode - will prevent executing send command or reading 1-wire sensor")
   parser.add_argument('--version', action='version', version='%(prog)s 0.2')
 
   parser.add_argument("city")
   parser.add_argument("count")
   args = parser.parse_args()
 
   if args.verbose    :  verbose_level = args.verbose
   if args.debug    :  debug_level = 1
 
   ow_city =   args.city     # set your city from command line
   ow_country   = "de"
   ow_appid     = "1f422f257ebc8ab249c166e634260f9d"
   ow_cnt       = args.count # maybe 6 - 16 not free will cost 400 USD/month
   ow_url_api   = "http://api.openweathermap.org/data/2.5/"
   ow_url_cur   = ow_url_api + "weather?q=" + ow_city + "," + ow_country + "&appid=" + ow_appid
   ow_url_fcst  = ow_url_api + "forecast?q=" + ow_city + "," + ow_country + "&appid=" + ow_appid
   ow_url_fcst16 = ow_url_api + "forecast/daily?q=" + ow_city + "," +ow_country + "&appid=" + ow_appid + "&cnt=" + ow_cnt
 
   ow_city = ow_city.lower()
   ow_file_cur = "ow_" + ow_city + "_cur.json"
   ow_file_for = "ow_" + ow_city + "_for.json"
   ow_file_for7 = "ow_" + ow_city + "_for7.json"
 
   # file_cur = open(ow_file_cur, 'w')
   # file_for = open(ow_file_for, 'w')
 
   print "--------------------- GET CURRENT DATA"
   if verbose_level > 1:
        print "# fetchHTML(): "
        print ow_url_cur
   try:
           print "URL - Request",
           req = urllib2.Request(ow_url_cur)
           print " - Open",
           response = urllib2.urlopen(req)
           print " - Read Response"
           output_cur  = response.read()
           #output   = fetchHTML(ow_url_cur)
           json_out_cur = json.loads(output_cur)
           # print json_out_cur
           if verbose_level > 2: pp.pprint(json_out_cur)
   except:
           print "Panic: cannot read url:", ow_url_cur
 
   print "--------------------- GET FORECAST DATA"
   if verbose_level > 1:
        print "# fetchHTML(): "
        print ow_url_fcst
   try:
           print "URL - Request", 
           req = urllib2.Request(ow_url_fcst)
           
           print "URL -Response", 
           response = urllib2.urlopen(req)
           
           print " - Read Response"
           output_fcst = response.read()
          
           json_out_fcst = json.loads(output_fcst)
           
           # print json_out_cur
           if verbose_level > 2: 
               pp.pprint(json_out_fcst)
               
   except:
           print "Panic: cannot read url:", ow_url_fcst
   
   try:
           print "URL -Reguest 16 days", 
           req16 = urllib2.Request(ow_url_fcst16) 
           print "URL-Response 16 days",
           response16= urllib2.urlopen(req16)
           output_fcst16 = response16.read()
           json_out_fcst16 = json.loads(output_fcst16)
           if verbose_level > 2: 
		        pp.pprint(json_out_fcst16)
   except:
          print "Panic: can't read url:", ow_url_fcst16
   print "dump json"
   with open(ow_file_cur, 'w') as outfile:
          json.dump(json_out_cur, outfile)
 
   with open(ow_file_for, 'w') as outfile:
          json.dump(json_out_fcst, outfile)
		  
   with open(ow_file_for7, 'w') as outfile:
          json.dump(json_out_fcst16, outfile)

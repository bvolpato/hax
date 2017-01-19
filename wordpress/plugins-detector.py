#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
from scrapy import *
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from urllib2 import urlopen
import zipfile
import json

plugins_file = open("plugins.json")
plugins = json.loads(plugins_file.read())

target = "http://TARGET/"

for plugin in plugins:
    
    phpFiles = filter(lambda pluginFile: "php" in pluginFile, plugins[plugin])
    phpFile = phpFiles[0]
    
    urlCheck = target + "/wp-content/plugins/" + phpFile
    try:
        
        req = urllib2.Request(urlCheck, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' })
        urlRes = urllib2.urlopen(req)
        
        print "[+] Worked", plugin, urlCheck
    except urllib2.HTTPError, e:
        #print "[-] Failed", plugin, urlCheck, e.code
        pass

print "Done!"
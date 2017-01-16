#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
from scrapy import *
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from urllib2 import urlopen
import zipfile
import json

plugins = {}

def getPlugins(url):
    global plugins
    
    urlRes = urlopen(url)
    res = HtmlResponse(url, body=urlRes.read())
    
    cards = res.css("div.plugin-card")
    
    for card in cards:
        try:
            
            link = card.css("h4 a").xpath("@href").extract()[0]
    
            linkRes = urlopen(link)
            
            pluginRes = HtmlResponse(url, body=linkRes.read())
            
            pluginName = pluginRes.css("h2[itemprop='name']").xpath("text()").extract()[0]
            downloadLink = pluginRes.css("a[itemprop='downloadUrl']").xpath("@href").extract()[0]
            
            fileName = downloadLink[downloadLink.rindex("/")+1:];
            filePath = "/tmp/" + fileName
            urllib.urlretrieve (downloadLink, filePath)
            
            zipFile = zipfile.ZipFile(filePath)
            
            files = zipFile.namelist()
            
            #phpFiles = filter(lambda pluginFile: "php" in pluginFile, files)
            
            plugins[pluginName] = files;
            print "Analyzed", pluginName, "-", fileName
            
        except Exception as e:
            print e
  
  
for i in range(1, 30):
    getPlugins("https://srd.wordpress.org/plugins/browse/popular/page/" + str(i) + "/");

with open("plugins.json", 'w+') as writeFile:
    writeFile.write(json.dumps(plugins, indent=4))

print "Done!"
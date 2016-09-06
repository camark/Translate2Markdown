#/usr/bin/env python3
#coding=utf8

import urllib
from urllib import request
from xml.dom.minidom import parse, parseString, Node

# http://dict-co.iciba.com/api/dictionary.php?w=go&key=0D90F9AF76633667613F22F9137AE868

urltemplate = "http://dict-co.iciba.com/api/dictionary.php?%s"

def getencodeurl(ew):
    return urltemplate % urllib.parse.urlencode({"w": ew, "key":"0D90F9AF76633667613F22F9137AE868"})

def parse(data):
    result = ""
    hasps = False
    hassent = False
    try:
        with parseString(data) as d:
            if(d.nodeType != Node.DOCUMENT_NODE):
                return None
            dictElement = d.getElementsByTagName("dict")[0]
            for item in dictElement.childNodes:
                if(item.nodeName == "#text"):
                    continue
                name = item.nodeName
                value = item.childNodes[0].nodeValue

                if(value is None):
                    if(name != "sent"):
                        continue
                    else:
                        pass
                if(name == "key"):
                    result += ("## %s\n```\n" % value)
                    key = value
                if(name == ("ps")):
                    if(not hasps):
                        result += ("[%s]\n" %value)
                        hasps = True
                # elif(name == "pron"):
                #     result += "[%s](%s)\n" %((key if(key) else "none"), value)
                elif(name == "pos"):
                    result += "%s  " % value
                elif(name == "acceptation"):
                    result += "%s" % value
                elif(name=="sent"):
                    if(not hassent):
                        hassent = True
                        result += "\n例句\n"

                    for i in item.childNodes:
                        n = i.nodeName
                        if(n == "#text"):
                            continue
                        v = i.childNodes[0].nodeValue
                        if(v is None):
                            continue
                        
                        if(n == "orig"):
                            result += v.strip('\n')
                        elif(n == "trans"):
                            result += v + "\n"
                        

            if(hasps):
                return result + "```"
            else:
                return None
    except Exception as e:
        print(e)
        return None

def translate(ew):
    url = getencodeurl(ew)
    result = None
    try:
        with urllib.request.urlopen(url) as f:
            result = parse(f.read().decode('utf-8'))
            f.close()
    except Exception as e:
        pass
    if(result is None):
        return ("# %s" % ew, False)
    else:
        return (result, True)
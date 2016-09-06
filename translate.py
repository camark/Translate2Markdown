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
    with urllib.request.urlopen(url) as f:
        result = parse(f.read().decode('utf-8'))
        f.close()
    if(result is None):
        return ("# %s" % ew, False)
    else:
        return (result, True)
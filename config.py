#/usr/bin/env python3
#coding=utf8

import configparser
import os

configfile = os.environ["HOME"] + "/.translate2markdown/config.conf"
defaultstoragepath = os.environ["HOME"] + "/Translate2markdown"

if(not os.path.exists(configfile)):
    os.makedirs(os.path.dirname(configfile),exist_ok=True)
    os.makedirs(defaultstoragepath, exist_ok=True)
    with open(configfile,"w") as f:
        f.write('''[global]
autosave = True
storagePath = %s
''' % defaultstoragepath)
        f.close()
    
parser = configparser.ConfigParser()
parser.read(configfile)

def isAutoSave():
    return True if(parser.get("global", "autosave")) == "True" else False

def setAutoSave(autosave):
    parser.set("global","autosave", value="True" if(autosave) else "False")
    with open(configfile,"w") as f:
        parser.write(f)
        f.close()

def getStoragePath():
    return parser.get("global", "storagePath")

def setStoragePath(path):
    parser.set("global", "storagePath", path)
    storagePath = path
    with open(configfile,"w") as f:
        parser.write(f)
        f.close()

storagePath = getStoragePath()

# License: zlib license
# see accompanying LICENSE file

# this desperately needs a nice solution

import sys, os, util
try:
  from _winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, CloseKey
except: pass

def regread(r, v, hkey = HKEY_LOCAL_MACHINE):
  if not "win32" in platforms:
    return ""
    
  print r, v
  #try:
  key = OpenKey(hkey, r)
  r = QueryValueEx(key, v)
  CloseKey(key)
  return r
  #except:
  #  return ""
  

def find_python():
  r = []
  
  for currentversion in "2.6 2.5 2.4 2.3 2.2 2.1 2.0 1.6 1.5".split():
    currentversion_nodots = currentversion.replace(".", "")
    
    names = ["python%s" % currentversion_nodots, "python%s" % currentversion]
    paths = [regread("SOFTWARE\\Python\\PythonCore\\%s" % currentversion, "InstallPath") + "/libs"]
    r.append((find_library(names, paths), []))
    
  return r
    
packages = {"python": find_python}
platforms = util.get_platforms()

def find_library(names, paths):
  return paths

def find_package(lib):
  #try:
  return packages[lib]()
  #except Exception, e:
  #  print e
  #  return None
    
#print "py:", find_package("python")

# License: zlib license
# see accompanying LICENSE file

# this desperately needs a nice solution

import sys, os

def find_library(names, paths):
  pass

def find_package(lib):
  if lib == "python":
    if sys.platform == "win32":
      if os.path.exists("C:\\Python26\\libs\\libpython26.a"):
        return ("C:\\Python26\\libs\\libpython26.a", "libpython26.a")
  
  return None
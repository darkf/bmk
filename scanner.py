# License: zlib license
# see accompanying LICENSE file
import re

class Scanner:
  rules  = {}
  comrx  = {}
  text   = ""
  pos    = 0
  
  def __init__(self, ignoreNone = False):
    self.ignoreNone = ignoreNone
  
  def setText(self, text):
    self.text = text
    
  def addText(self, text):
    self.text += text
  
  def addRule(self, rule, tok):
    self.rules[rule] = tok
    
  def getToken(self, advance = True):
    if self.text[self.pos:] == '': # no more text to cover
      raise StopIteration
    
    for k,v in self.rules.iteritems():
      try:
        m = self.comrx[k].match(self.text, self.pos)
      except KeyError:
        self.comrx[k] = re.compile(k) # compile regex
        m = self.comrx[k].match(self.text, self.pos)
      
      if not m: # no match
        continue
      
      #print "matched '%s' -> '%s'" % (k, m.group(0))
      if advance:
        self.pos = m.end()
      
      if callable(v):
        v = v(m.group)
        
        if v is None and self.ignoreNone: # ignore it and get new token
          return self.getToken()
        
      return v
      
    raise StopIteration
    
  def peek(self):
    return self.getToken(False)
    
  def next(self):
    return self.getToken()
    
  def __iter__(self):
    return self
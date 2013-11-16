import os, pickle, xbmc, os.path
from datetime import datetime

class Cache(object):
  
  def __init__(self, settings):
    addonPath = settings.getAddonInfo('path')
    self.cacheDir = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/'), os.path.basename(addonPath))
    self.createCacheDir()

  def createCacheDir(self):
    if os.path.isdir(self.cacheDir) == False:
      os.makedirs(self.cacheDir)

  def write_cache(self, name, obj):
    path = os.path.join(self.cacheDir, name)
    with open(path, 'wb') as cache_file:
      pickle.dump(obj, cache_file)
        
  def isExpired(self, name, maxCacheAge):
    cacheFile = os.path.join(self.cacheDir, name)
    try:
      lastModified = datetime.fromtimestamp(os.path.getmtime(cacheFile))
      cacheAge = (datetime.now() - lastModified).seconds / 60
      return cacheAge > maxCacheAge
    except OSError:
      return True
      
  def load_cache(self, name):
    path = os.path.join(self.cacheDir, name)
    with open(path, 'rb') as cache:
      return pickle.load(cache)

import os, pickle
from datetime import *

class Cache(object):
  
  def __init__(self, settings):
    addonPath = settings.getAddonInfo('path')
    self.cacheDir = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/'), os.path.basename(addonPath))
    createCacheDir()

  def createCacheDir(self):
    if os.path.isdir(self.cacheDir) == False:
      os.makedirs(self.cacheDir)

  def write_cache(self, name, obj):
    path = os.path.join(self.cacheDir, name)
    exp_path = os.path.join(self.cacheDir, name+'.exp')
    f = open(path, 'wb')
    pickle.dump(obj, f)
    f.close()
    f = open(exp_path, 'wb')
    pickle.dump(datetime.now(), f)
    f.close()
        
  def get_cache_age(self, name):
    path = os.path.join(self.cacheDir, name+'.exp')
    f = open(path, 'rb')
    exp = pickle.load(f)
    f.close()
    return (datetime.now() - exp).seconds / 60
      
  def load_cache(self, name):
    path = os.path.join(self.cacheDir, name)
    f = open(path, 'rb')
    ret = pickle.load(f)
    f.close()
    return ret

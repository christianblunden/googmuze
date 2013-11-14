import sys, os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib

ID_PARAM = "id"
TITLE_PARAM = "title"

__settings__   = xbmcaddon.Addon(id='plugin.audio.googmuze')
__cwd__        = __settings__.getAddonInfo('path')
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )
__pluginHandle__ = int(sys.argv[1])

sys.path.append (__resource__)
print(__resource__)
sys.path.append('/home/christian/.xbmc/addons/plugin.audio.googmuze/resources/lib/')
from gmusicapi import Webclient

def googleMusicConnect():
  username = __settings__.getSetting('username')
  password = __settings__.getSetting('password')
  api = Webclient()
  api.login(username,password)
  return api

def parseParams(parameters):
  paramDict = {}
  if parameters:
      paramPairs = parameters[1:].split("&")
      for paramsPair in paramPairs:
        paramSplits = paramsPair.split('=')
        if (len(paramSplits)) == 2:
          paramDict[paramSplits[0]] = paramSplits[1]
  return paramDict

def playSong(params,api):
  songId = params.get(ID_PARAM,None)
  title = params.get(TITLE_PARAM,None)
  link = api.get_stream_urls(songId)[0]
  li = xbmcgui.ListItem(label=title, path=link)
  li.setInfo(type='Audio', infoLabels={ "Title": title })
  xbmc.Player().play(item=link, listitem=li)

def addMenuItem(track):
  caption = track['artistNorm'] + " - " + track['titleNorm']
  listItem = xbmcgui.ListItem(caption)
  listItem.setInfo(type="Audio", infoLabels={ "Title": caption })
  url = sys.argv[0] + '?' + urllib.urlencode({ID_PARAM:track['id'].encode('utf-8'),TITLE_PARAM:caption.encode('utf-8')})
  print("Song Url:%s"%url)
  return xbmcplugin.addDirectoryItem(handle=__pluginHandle__, url=url, listitem=listItem)

def buildMenu(api):
  library = api.get_all_songs()
  for track in library[:100]:
    addMenuItem(track)
  xbmcplugin.endOfDirectory(__pluginHandle__)

api = googleMusicConnect()

if not sys.argv[2]:
  buildMenu(api)
else:
  params = parseParams(sys.argv[2])
  playSong(params,api)

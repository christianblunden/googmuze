import xbmcgui, xbmcplugin
import urllib, urlparse

class Navigation(object):
  ACTION = 'action'
  SONG_ID = 'song_id'
  SONG_TITLE = 'song_title'

  MAIN_MENU = 0
  ALL_SONGS = 1
  PLAYLISTS = 2
  PLAY_SONG = 10

  NAVIGATION = { MAIN_MENU:mainMenu,
                 ALL_SONGS:listAllSongs,
                 PLAYLISTS:listPlaylists,
                 PLAY_SONG:playSong }

  def __init__(self, library):
    self.library = library

  def parse_request(self, request):
    params = urlparse.parse_qs(request)
    return dict((k,v[0]) for (k,v) in params.iteritems())

  def process_request(self, request):
    parameters = self.parse_request(request)
    action = int(parameters.get(ACTION, MAIN_MENU))
    NAVIGATION[action](parameters)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)

  def folderItem(self, title, params):
    li = xbmcgui.ListItem(label=title)
    li.setProperty("Folder", "true")
    url = sys.argv[0] + '?' + urllib.urlencode(params)
    return url,li,"true"

  def songItem(self, track):
    songId = track['id'].encode('utf-8')
    songTitle = (track['artistNorm'] + " - " + track['titleNorm']).encode('utf-8')
    li = xbmcgui.ListItem(songTitle)
    li.setInfo(type="Audio", infoLabels={ "Title": songTitle })
    url = sys.argv[0] + '?' + urllib.urlencode({ACTION:PLAY_SONG,SONG_ID:songId,SONG_TITLE:songTitle})
    return url,li

  def mainMenu(self, parameters):
    menuItems = []
    menuItems.append(self.folderItem("Main Menu", {ACTION:MAIN_MENU}))
    menuItems.append(self.folderItem("All Songs", {ACTION:ALL_SONGS}))
    menuItems.append(self.folderItem("Playlists", {ACTION:PLAYLISTS}))
    xbmcplugin.addDirectoryItems(handle=int(sys.argv[1]), menuItems)

  def listAllSongs(self, parameters):
    songItems = self.library.allSongs().map(lambda track: self.songItem(track))
    xbmcplugin.addDirectoryItems(handle=int(sys.argv[1]), menuItems)

  def listPlaylists(self, parameters):
    print("listPlaylists")

  def playSong(self, parameters):
    title = parameters.get(SONG_TITLE, None)
    link = self.client.get_stream_urls(parameters.get(SONG_ID, None))[0]
    li = xbmcgui.ListItem(label=title, path=link)
    li.setInfo(type='Music', infoLabels={"Title": title})
    xbmc.Player().play(item=link, listitem=li)


import xbmc, xbmcgui, xbmcplugin
import sys, urllib, urlparse

class Navigation(object):
  ACTION = 'action'
  SONG_ID = 'song_id'
  SONG_TITLE = 'song_title'

  MAIN_MENU = 0
  ALL_SONGS = 1
  PLAYLISTS = 2
  PLAY_SONG = 10

  def __init__(self, library):
    self.library = library
    self.actions = { Navigation.MAIN_MENU:self.mainMenu,
                     Navigation.ALL_SONGS:self.listAllSongs,
                     Navigation.PLAYLISTS:self.listPlaylists,
                     Navigation.PLAY_SONG:self.playSong }

  def parse_request(self, request):
    params = urlparse.parse_qs(request[1:])
    return dict((k,v[0]) for (k,v) in params.iteritems())

  def process_request(self, request):
    parameters = self.parse_request(request)
    action = int(parameters.get(Navigation.ACTION, Navigation.MAIN_MENU))
    self.actions[action](parameters)
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
    url = sys.argv[0] + '?' + urllib.urlencode({Navigation.ACTION:Navigation.PLAY_SONG,Navigation.SONG_ID:songId,Navigation.SONG_TITLE:songTitle})
    return url,li

  def mainMenu(self, parameters):
    menuItems = []
    menuItems.append(self.folderItem("Main Menu", {Navigation.ACTION:Navigation.MAIN_MENU}))
    menuItems.append(self.folderItem("All Songs", {Navigation.ACTION:Navigation.ALL_SONGS}))
    menuItems.append(self.folderItem("Playlists", {Navigation.ACTION:Navigation.PLAYLISTS}))
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), menuItems)

  def listAllSongs(self, parameters):
    songItems = [self.songItem(track) for track in self.library.allSongs()]
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), songItems)

  def listPlaylists(self, parameters):
    print("listPlaylists")

  def playSong(self, parameters):
    title = parameters.get(Navigation.SONG_TITLE, None)
    link = self.library.songStreamUrl(parameters.get(Navigation.SONG_ID, None))
    li = xbmcgui.ListItem(label=title, path=link)
    li.setInfo(type='Music', infoLabels={"Title": title})
    xbmc.Player().play(item=link, listitem=li)


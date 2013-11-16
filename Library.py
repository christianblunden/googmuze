from gmusicapi import Webclient

class Library(object):

  def __init__(self, addon):
    self.client = self.createClient(addon)

  def createClient(self, settings):
    username = settings.getSetting('username')
    password = settings.getSetting('password')
    client = Webclient()
    client.login(username,password)
    return client

  def allSongs(self):
    return self.client.get_all_songs()

  def songStreamUrl(self, songId):
    return self.client.get_stream_urls(songId)[0]

  def playlists(self):
    playlists = self.client.get_all_playlist_ids(auto=False,user=True)['user']
    return dict([(ids[0],name) for name,ids in playlists.items()])

  def playlistSongs(self, playlistId):
    return self.client.get_playlist_songs(playlistId)
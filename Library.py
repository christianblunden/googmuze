from gmusicapi import Webclient
import Cache

class Library(object):
  CACHE_TIME = 60

  def __init__(self, settings, cache):
    self.client = self.createClient(settings)
    self.cache = cache

  def createClient(self, settings):
    username = settings.getSetting('username')
    password = settings.getSetting('password')
    client = Webclient()
    client.login(username,password)
    return client

  def allSongs(self):
    if cacheExpired('songs'):
      self.cache.write_cache('songs', self.client.get_all_songs())
    return self.cache.load_cache('songs')

  def songStreamUrl(self, songId):
    return self.client.get_stream_urls(songId)[0]

  def playlists(self):
    if cacheExpired('playlists'):
      playlists = self.client.get_all_playlist_ids(auto=False,user=True)['user']
      self.cache.write_cache('playlists',  dict([(ids[0],name) for name,ids in playlists.items()]))
    return self.cache.load_cache('playlists')

  def playlistSongs(self, playlistId):
    cacheKey = 'playlist'+playlistId
    if cacheExpired(cacheKey):
      self.cache.write_cache(cacheKey, self.client.get_playlist_songs(playlistId))
    return self.cache.load_cache(cacheKey)

  def cacheExpired(self,key):
    return self.cache.get_cache_age(key) > Library.CACHE_TIME
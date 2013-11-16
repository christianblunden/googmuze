from gmusicapi import Webclient

class Library(object):

  def __init__(self, addon):
    self.client = self.createClient(addon)

  def createClient(self, settings):
    username = __settings__.getSetting('username')
    password = __settings__.getSetting('password')
    client = Webclient()
    client.login(username,password)
    return client

  def allSongs(self):
    return self.client.get_all_songs()

import sys, os
import xbmc, xbmcaddon

settings   = xbmcaddon.Addon(id='plugin.audio.googmuze')
resource   = xbmc.translatePath(os.path.join(settings.getAddonInfo('path'), 'resources', 'lib'))
sys.path.append(resource)

import Library, Navigation, Cache

library = Library.Library(settings, Cache.Cache(settings))

nav = Navigation.Navigation(library)
nav.process_request(sys.argv[2])

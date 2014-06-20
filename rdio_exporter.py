#!/usr/bin/env python

import csv
import unicodedata
import urllib2

import rdio
import credentials


def Normalize(value):
	return unicodedata.normalize('NFKD', value).encode('ascii','ignore')


rdio_client = rdio.Rdio(credentials.CREDENTIALS)

try:
  url = rdio_client.begin_authentication('oob')
  print('Go to: ' + url)

  verification = str(input('Then enter the code: ')).strip()
  rdio_client.complete_authentication(verification)

  playlists = rdio_client.call('getPlaylists', params={'extras': 'tracks'})['result']['owned']

  for playlist in playlists:
  	tracks = []
  	for track in playlist['tracks']:
  		tracks.append((
  			Normalize(track['artist']),
  			Normalize(track['album']),
  			Normalize(track['name']))
  		)

  	tracks.sort()
  	filename = playlist['name'].lower().replace(' ', '_') + '.csv'
  	with open(filename, 'w+') as fh:
  		writer = csv.writer(fh)
  		writer.writerow(['artist', 'album', 'track'])
  		writer.writerows(tracks)
  	print 'Wrote playlist "%s" to %s' % (playlist['name'], filename)

except urllib2.HTTPError as ex:
  print(ex.read())

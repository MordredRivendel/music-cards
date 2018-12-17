#!/usr/bin/env python
from mpd import MPDClient
#from readtest import *
import re
from CardList import CardList
from Reader import Reader
import sys


def connectMPD():
	try:
		client = MPDClient()               # create client object
		client.timeout = 200               # network timeout in seconds (floats allowed), default: None
		client.idletimeout = None  
		print "Connecting..."
		client.connect("localhost", 6600) 
		print "Connected!"
		return client
	except:
		print 'Could not connect to MPD server'

def play(client, plist):
	try:
		client.stop()
		client.clear()
		client.add(plist)
		if re.search('playlist',plist):
			client.shuffle()
		client.play()
		print 'play'
	except:
		print 'Could not play %s' % plist 

def playlist(client, plist):
	try:
		client.stop()
		client.clear()
		client.load(plist)
		client.play()
		print 'playlist'
	except:
		print 'Could not play playlist %s' % plist 
		
reader = Reader()
cardList = CardList()

print 'Ready: place a card on top of the reader'
autostart = 'file://var/lib/mopidy/network/music/start.mp3'    # autostart funktion
if autostart != '':
	client = connectMPD()
	client.stop()
	client.clear()
	client.add(autostart)
	client.close()

while True:
	try:
		card = reader.readCard()
		print 'Read card', card
		plist = cardList.getPlaylist(card)
		print 'Playlist', plist
		print '.m3u' in plist
		if plist != '':
			client = connectMPD()
			if plist=='pause':
				client.pause()
			elif plist=='next':                 #next song
                                client.next()
                        elif plist=='play':                 #play song
                                client.play()
                        elif plist=='previous':             #previous song
                                client.previous()
                        elif plist=='shuffle':              #turn on/off shuffle
                                client.shuffle()
                        elif plist=='voldown':              #volume down in steps
                                client.status()['volume']
                                client.status()['state']
                                level = int(client.status()['volume']) - 10 #change to desired amount for decreasing volume
                                level = max(min(level, 100), 0)
                                client.setvol(level)
                                client.status()['volume']
                        elif plist=='volup':                #volume up in steps
                                client.status()['volume']
                                client.status()['state']
                                level = int(client.status()['volume']) + 10 #change to desired amount for increasing volume
                                level = max(min(level, 100), 0)
                                client.setvol(level)
                                client.status()['volume']
                        elif plist=='mute':                 #volume mute
                                client.setvol(0)
			elif ':' in plist:                 #URI
                                play(client, plist)
                        else:					# open Playlist
                                playlist(client, plist)
			client.close()
	except KeyboardInterrupt:
		sys.exit(0)
	except:
		pass

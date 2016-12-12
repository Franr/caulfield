# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import commands


class PlayerClosed(Exception):
    pass


class PlayerPaused(Exception):
    pass


class SameTrack(Exception):
    pass


class WMCtrlData(object):
    COMMAND = "wmctrl -lx | awk '/spotify.Spotify/ {print $0}'"
    PLAYER_NAME = 'Spotify'
    # possible status
    CLOSED = 'CLOSED'
    PAUSED = 'PAUSED'
    PLAYING = None

    def __init__(self, lyric_source):
        self.lyric_source = lyric_source
        self.artist = ''
        self.title = ''
        self.lyrics = ''
        self.updated = False
        self.status = self.CLOSED

    def set_status(self, status):
        self.status = status

    def get_info(self):
        raw_output = commands.getoutput(self.COMMAND)
        if raw_output == '':
            raise PlayerClosed

        # processing command output
        _hostname = commands.getoutput('hostname')
        # right now the string is something like this
        # "<numbers>  <number> spotify.Spotify <hostname> <author> - <track>"
        # then we need to split using the hostname
        output = raw_output.decode('utf-8').split(_hostname)[1].lstrip()
        if output == self.PLAYER_NAME:
            raise PlayerPaused

        try:
            # WARNING: if there is more than one " - " on the string, will explode
            artist, title = output.split(" - ")
        except ValueError:
            # an ugly workaround for an untested case
            # at least it won't break
            artist, title = self.artist, self.title

        if (self.artist, self.title) == (artist, title):
            raise SameTrack

        return artist, title

    def process(self):
        self.updated = False
        try:
            current_artist, current_title = self.get_info()
        except PlayerClosed:
            self.set_status(self.CLOSED)
        except PlayerPaused:
            self.set_status(self.PAUSED)
        except SameTrack:
            return
        else:
            self.set_status(self.PLAYING)
            self.lyrics = self.lyric_source(current_artist, current_title).lyric
            self.artist, self.title = current_artist, current_title
        self.updated = True

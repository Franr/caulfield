# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import requests


class MusixMatchLyric(object):
    ENDPOINT = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

    @property
    def api_key(self):
        from config import musixmatch_apikey
        return musixmatch_apikey

    @property
    def lyric(self):
        payload = {
            'q_artist': self.artist,
            'q_track': self.title,
            'apikey': self.api_key,
        }
        try:
            response = requests.get(self.ENDPOINT, payload).json()
            lyric = response['message']['body']['lyrics']['lyrics_body']
        except (requests.RequestException, KeyError, TypeError):
            return "### bad request ###\n{}\n{}".format(self.ENDPOINT, payload)
        else:
            return lyric

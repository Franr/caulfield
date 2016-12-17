#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from lyric_source import MusixMatchLyric
from data_source import WMCtrlData
from gui import run_ui


if __name__ == '__main__':
    run_ui(WMCtrlData, MusixMatchLyric)

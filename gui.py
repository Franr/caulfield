# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from contextlib import contextmanager
from Tkinter import Tk, Text, BOTH, END, DISABLED, NORMAL
from ttk import Frame


@contextmanager
def widget_locker(widget):
    try:
        widget.config(state=NORMAL)
        yield
    finally:
        widget.config(state=DISABLED)


class GUI(Frame):

    def __init__(self, parent, data_source, lyric_source):
        Frame.__init__(self, parent)
        self.parent = parent
        self.data = data_source(lyric_source)
        # UI
        self.pack(fill=BOTH, expand=True)
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, pady=5, padx=5, expand=True)
        self.txt.after(500, self.refresh_lyric)

    def update_window_title(self):
        title = "{} - {}".format(self.data.artist, self.data.title)
        if self.data.status:
            title += " [{}]".format(self.data.status)
        self.parent.title(title)

    def refresh_lyric(self):
        self.data.process()
        if self.data.updated:
            self.update_window_title()
            with widget_locker(self.txt):
                self.txt.delete(1.0, END)
                self.txt.insert(END, self.data.lyrics)
                self.txt.update()
        self.txt.after(500, self.refresh_lyric)


def run_ui(data_source, lyric_source):
    root = Tk()
    root.geometry('400x400')
    root.title('claufield')
    GUI(root, data_source, lyric_source)
    root.mainloop()

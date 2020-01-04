#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import sys
import tkinter as tk
from layout import LayoutGUI
from widget import Widget
from contansts import Place


class Wizard:

    def __init__(self, parent: tk.Tk):
        self.parent = parent
        # self.parent.iconbitmap(Wizard.resource_path("resource/icon.ico"))
        self.parent.title('测试窗口')
        self.parent.resizable(width=False, height=False)
        self.window_width = 800
        self.window_height = 700
        self.layout_utils = LayoutGUI(self.window_width)
        self.widget = Widget(root=self.parent, layout_utils=self.layout_utils)

        self.center_layout()

    def center_layout(self):
        screenwidth = self.parent.winfo_screenwidth()
        screenheight = self.parent.winfo_screenheight()
        size = '%dx%d+%d+%d' % (
            self.window_width,
            self.window_height,
            (screenwidth - self.window_width) / 2,
            (screenheight - self.window_height) / 2
        )
        self.parent.geometry(size)

    @staticmethod
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    root = tk.Tk()
    app = Wizard(root)
    root.mainloop()

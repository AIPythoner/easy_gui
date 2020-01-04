#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from layout import LayoutGUI
import tkinter as tk
import tkinter.ttk as ttk
from contansts import Place, VAL_TYPE_MAP
from utils import contains_unicode, split_char, calc_width


class Widget(object):

    def __init__(self, root, layout_utils: LayoutGUI):
        self.root = root
        self.layout_utils = layout_utils

    @staticmethod
    def widget_height(text):
        return 25 if contains_unicode(text) else 20

    def label(self, prev, place: Place, text: str):
        label: ttk.Label = ttk.Label(self.root, text=text, anchor=tk.W)
        label_height = self.widget_height(text)
        label_width = calc_width(text, 15, 7.5)

        self.layout_utils.widget_place(
            src=label,
            prev=prev,
            place=place,
            width=label_width,
            height=label_height,
            tiny_space=False
        )
        return label

    def entry(self, prev, place: Place, title: str, width, default=None, val_type=int):
        label: ttk.Label = self.label(prev, place, title)
        label_height = self.widget_height(title)
        val: tk.Variable = VAL_TYPE_MAP.get(val_type)()
        val.set(default)
        entry: ttk.Entry = ttk.Entry(self.root, textvariable=val, justify=tk.LEFT)
        self.layout_utils.next_to_widget(
            src=entry,
            target=label,
            width=width,
            height=label_height,
            tiny_space=True,
        )
        return label, val, entry

    def combobox(
            self,
            prev,
            place: Place,
            title: str,
            options,
            current=1,
            editable=False,
            blank_click_callback=None,
            selected_callback=None,
            fill_callback=None,
            click_callback=None
    ):
        label: ttk.Label = self.label(prev, place, title)
        if not editable:
            combobox: ttk.Combobox = ttk.Combobox(
                self.root, values=tuple(options) if options else None, state='readonly'
            )
        else:
            combobox: ttk.Combobox = ttk.Combobox(
                self.root, values=tuple(options) if options else None
            )

        combobox.current(current)

        # 被选中回调
        if selected_callback:
            combobox.bind("<<ComboboxSelected>>", lambda x: selected_callback(x))
        max_length = max([calc_width(i, 15, 7.5) for i in options])
        combobox_height = 30 if contains_unicode(options[0]) else 20

        # 空白处回调
        if blank_click_callback:
            self.root.bind('<Button-1>', lambda x: blank_click_callback(x))

        # 填充回调
        if fill_callback:
            combobox.bind(
                sequence="<Return>",
                func=lambda x: fill_callback(x)
            )

        # 点击回调
        if click_callback:
            combobox.bind(
                sequence="<Button-1>",
                func=lambda x: click_callback(x)
            )

        self.layout_utils.next_to_widget(
            src=combobox,
            target=label,
            width=max_length + 25,
            height=combobox_height,
            tiny_space=True,

        )
        return label, combobox

    def listbox(self, prev, place: Place, title: str, width, height, delete_callback=None):
        label: ttk.Label = self.label(prev, place, title)
        listbox: tk.Listbox = tk.Listbox(self.root, font=('微软雅黑', 9))

        def delete_event(event, obj: tk.Listbox, callback=None):
            i = obj.curselection()[0]
            obj.delete(i)
            if callback:
                callback()

        def listbox_scrollbar(obj: tk.Listbox):
            y_scrollbar = tk.Scrollbar(
                obj, command=listbox.yview
            )
            y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            obj.config(yscrollcommand=y_scrollbar.set)

        self.layout_utils.next_to_widget(
            src=listbox,
            target=label,
            width=width,
            height=height,
            tiny_space=True
        )
        listbox.bind(
            sequence="<Delete>",
            func=lambda x: delete_event(x, delete_callback)
        )
        listbox_scrollbar(listbox)
        return label, listbox

    def button(self, prev, place: Place, title: str, callback):

        if callback:
            button: ttk.Button = ttk.Button(
                self.root, text=title, command=lambda: callback()
            )
        else:
            button: ttk.Button = ttk.Button(
                self.root, text=title
            )

        btn_height = 30 if contains_unicode(title) else 20
        uchar_len, char_len = split_char(title)
        btn_width = int(uchar_len * 15 + char_len * 7.5)

        self.layout_utils.widget_place(
            src=button,
            prev=prev,
            place=place,
            width=btn_width * 1.8,
            height=btn_height,
            tiny_space=True
        )
        return button

    def label_frame(self, prev, place: Place, title: str, width, height, tiny_space=True):
        label_frame: ttk.Labelframe = ttk.Labelframe(self.root, text=title)
        self.layout_utils.widget_place(
            src=label_frame,
            prev=prev,
            place=place,
            width=width,
            height=height,
            tiny_space=tiny_space
        )
        return label_frame

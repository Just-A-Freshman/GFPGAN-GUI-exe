import tkinter as tk
from tkinter.ttk import Scrollbar, Style
from typing import Literal


class BorderlessScrollbar(Scrollbar):
    _style_map = {
        "thumb_color": ("background", "lightcolor", "darkcolor"),
        "troughcolor": ("troughcolor", "bordercolor"),
        "arrowcolor": "arrowcolor",
        "gripcount": "gripcount"
    }

    def __init__(
            self,
            master,
            orient: Literal["vertical", "horizontal"] = "vertical",
            troughcolor="",
            arrowcolor="white",
            thumb_color="#A8A8A8",
            highlight_bg="#9C9C9C",
            show_thumb=True,
            gripcount=0,
            **kwargs
    ):
        troughcolor = troughcolor if troughcolor else master.cget("bg")
        self.__show_thumb = show_thumb
        self.__orient = orient
        if self.__show_thumb:
            self.master: tk.Widget = master
        else:
            self.master: tk.Frame = tk.Frame(master, bg=troughcolor)
            self.master.bind('<Configure>', self.on_configure)

        super().__init__(self.master, orient=orient, **kwargs)
        self.__style = Style()
        # thumb_color指的是滑块的背景色, troughcolor指槽的颜色
        self.config(
            troughcolor=troughcolor, arrowcolor=arrowcolor, thumb_color=thumb_color,
            highlight_bg=highlight_bg, gripcount=gripcount,
        )

    def config(self, **kwargs):
        highlight_bg = kwargs.pop("highlight_bg", None)
        command = kwargs.pop("command", None)
        if highlight_bg is not None:
            self.__style.map("TScrollbar", background=[('active', highlight_bg)])
        if command is not None:
            super().config(command=command)

        style_dict = {}
        for prop, value in kwargs.items():
            if prop not in BorderlessScrollbar._style_map.keys():
                continue
            style_keys = self._style_map.get(prop)
            if style_keys:
                if isinstance(style_keys, tuple):
                    for style_key in style_keys:
                        style_dict[style_key] = value
                else:
                    style_dict[style_keys] = value
            else:
                style_dict[prop] = value

        self.__style.configure("Vertical.TScrollbar", **style_dict)
        self.__style.configure("Horizontal.TScrollbar", **style_dict)

    def on_configure(self, _):
        if self.__orient == "vertical":
            self.__place(height=self.master.winfo_height() + 32)
        else:
            self.__place(width=self.master.winfo_width() + 32)

    def layout(self, func_name: str):
        def inner(*args, **kwargs):
            if self.__show_thumb:
                getattr(super(BorderlessScrollbar, self), func_name)(*args, **kwargs)
                return
            getattr(self.master, func_name)(*args, **kwargs)
            self.master.update()
            if self.__orient == "vertical":
                self.master.config(width=13)
                self.__place(y=-16, height=self.master.winfo_height() + 32)
            else:
                self.master.config(height=13)
                self.__place(x=-16, width=self.master.winfo_width() + 32)
        return inner

    def __place(self, *args, **kwargs):
        super().place(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.layout("pack")(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.layout("place")(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.layout("grid")(*args, **kwargs)


if __name__ == "__main__":
    from tkinter_extension.Widget.TreeView import FileTreeView
    root_window = tk.Tk()
    root_window.configure(background="black")
    root_window.geometry("306x400+400+400")
    FileTreeView.load_ico_img()
    treeview = FileTreeView(root_window)
    treeview.build_catalog_tree(r"D:\Users\pbl\Desktop\superFolder")
    treeview.place(width=310, height=400)
    v_scrollbar = BorderlessScrollbar(
        root_window, orient="vertical", command=treeview.yview, cursor="hand2",
        troughcolor="#3B3B3B", thumb_color="#616161", show_thumb=False
    )
    v_scrollbar.pack(side="right", fill="both")
    treeview.configure(yscrollcommand=v_scrollbar.set)
    root_window.mainloop()

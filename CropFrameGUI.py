from ThemeWidget import (Frame, ThemeCanvas, Label)
from tkinter_extension.Widget.Button import FlatButton
from tkinter_extension.Widget.Entry import CustomEntry
from tkinter_extension.Widget.Canvas import ToningCanvas
from tkinter_extension.Widget.TreeView import FileTreeView
from tkinter_extension.Widget.ContextMenu import FileMenu
from tkinter_extension.Widget.Scrollbar import BorderlessScrollbar
from Config import Theme
from os import path


class CropFrame(object):
    def __init__(self, parent):
        self.parent: Frame = parent
        self.main_canvas = self.__set_main_canvas()
        self.undo_btn = self.__set_undo_btn()
        self.redo_btn = self.__set_redo_btn()
        self.tree_view = self.__set_tree_view()
        self.file_menu = self.__set_file_menu()
        self.tree_v_scrollbar = self.__set_treeview_vertical_scrollbar()
        self.tree_h_scrollbar = self.__set_treeview_horizontal_scrollbar()
        self.canvas_h_scrollbar = self.__set_canvas_horizontal_scrollbar()
        self.search_entry = self.__set_search_entry()
        self.search_btn = self.__set_search_btn()
        self.open_file_btn = self.__set_open_new_file_btn()
        self.open_folder_btn = self.__set_open_new_folder_btn()
        self.execute_btn = self.__set_execute_btn()
        self.export_btn = self.__set_export_btn()
        self.export_entry = self.__set_export_entry()
        self.choose_export_folder_btn = self.__set_choose_export_folder_btn()
        self.tip_label1 = self.__set_export_file_tip()
        self.toning_canvas = self.__set_toning_canvas()

    def __set_main_canvas(self):
        canvas = ThemeCanvas(self.parent)
        canvas.place(x=262, y=78, width=638, height=423)
        return canvas

    def __set_undo_btn(self):
        btn = FlatButton(self.parent, text="\u21A9", font=Theme.font_box[9],
                         **Theme.style_dict["FlatButton-1"])
        btn.place(x=262, y=39, height=39, width=72)
        return btn

    def __set_redo_btn(self):
        btn = FlatButton(self.parent, text="\u21AA", font=Theme.font_box[9],
                         **Theme.style_dict["FlatButton-1"])
        btn.place(x=334, y=39, height=39, width=71)
        return btn

    def __set_search_entry(self):
        entry = CustomEntry(
            self.parent, font=Theme.font_box[2], start_pos=37,
            **Theme.style_dict["Entry-1"]
        )
        entry.place(x=0, y=39, width=262, height=39)
        return entry

    def __set_search_btn(self):
        button = FlatButton(self.parent, **Theme.style_dict["FlatButton-4"])
        button.config_img(path.abspath(r"Data\ico\Light_search.png"))
        button.place(x=1, y=40, height=37, width=38)
        return button

    def __set_open_new_folder_btn(self):
        button = FlatButton(self.parent, text="打开文件夹", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=0, y=0, height=39, width=131)
        return button

    def __set_open_new_file_btn(self):
        button = FlatButton(self.parent, text="打开图片", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=131, y=0, height=39, width=131)
        return button

    def __set_tree_view(self):
        FileTreeView.load_ico_img()
        tree_view = FileTreeView(self.parent, **Theme.style_dict["TreeView"])
        tree_view.column("#0", minwidth=1200, width=1200)
        tree_view.place(x=-2, y=77, width=264, height=424)
        return tree_view

    def __set_file_menu(self):
        file_menu = FileMenu(self.parent, font=Theme.font_box[2])
        return file_menu

    def __set_treeview_vertical_scrollbar(self):
        scrollbar = BorderlessScrollbar(
            self.parent, show_thumb=False, cursor="hand2",
            **Theme.style_dict["Scrollbar"]
        )
        scrollbar.place(x=261, y=78, height=410)
        return scrollbar

    def __set_treeview_horizontal_scrollbar(self):
        scrollbar = BorderlessScrollbar(
            self.parent, show_thumb=False, cursor="hand2",
            orient="horizontal", **Theme.style_dict["Scrollbar"]
        )
        scrollbar.place(x=-1, y=488, width=263, height=13)
        return scrollbar

    def __set_canvas_horizontal_scrollbar(self):
        scrollbar = BorderlessScrollbar(
            self.parent, show_thumb=False, cursor="hand2",
            orient="horizontal", **Theme.style_dict["Scrollbar"]
        )
        scrollbar.place(x=274, y=488, width=626, height=14)
        return scrollbar

    def __set_export_btn(self):
        button = FlatButton(self.parent, text="导出文件", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=529, y=39, width=131, height=39)
        return button

    def __set_execute_btn(self):
        button = FlatButton(self.parent, text="立刻处理", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=405, y=39, width=131, height=39)
        return button

    def __set_export_file_tip(self):
        label = Label(self.parent, text="文件导出路径:", font=Theme.font_box[4],
                      **Theme.style_dict["Label"])
        label.place(x=267, y=3, width=131)
        return label

    def __set_choose_export_folder_btn(self):
        button = FlatButton(self.parent, text="选择文件夹", font=Theme.font_box[1],
                            **Theme.style_dict["FlatButton-3"])
        button.place(x=660, y=3, height=36, width=100)
        return button

    def __set_export_entry(self):
        entry = CustomEntry(self.parent, font=Theme.font_box[1], **Theme.style_dict["Entry-1"])
        entry.place(x=405, y=3, width=255, height=36)
        return entry

    def __set_toning_canvas(self):
        canvas = ToningCanvas(self.parent, bg=Theme.win_bg, colours=[
            "#FFFFFF", "#000000", "#FF0000", "#00FF00",
            "#0000FF", "#FFFF00", "#FFA500", "#9B30FF"
        ])
        canvas.place(x=664, y=45, height=30, width=230)
        return canvas

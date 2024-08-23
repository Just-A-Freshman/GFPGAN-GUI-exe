from ThemeWidget import (Frame, ThemeCanvas, ThemeButton, FileTreeView, ThemeEntry,
                         ThemeLabel, PushButton, ToningCanvas)
from os import path


class CropFrame(object):
    def __init__(self, parent):
        self.parent: Frame = parent
        self.main_canvas = self.__set_main_canvas()
        self.undo_btn = self.__set_undo_btn()
        self.redo_btn = self.__set_redo_btn()
        self.tree_view = self.__set_tree_view()
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
        btn = ThemeButton(self.parent, text="\u21A9", font=("Segoe UI", 36, "bold"))
        btn.place(x=262, y=39, height=39, width=72)
        return btn

    def __set_redo_btn(self):
        btn = ThemeButton(self.parent, text="\u21AA", font=("Segoe UI", 36, "bold"))
        btn.place(x=334, y=39, height=39, width=71)
        return btn

    def __set_search_entry(self):
        entry = ThemeEntry(self.parent, font=("微软雅黑", 14))
        entry.start_pos = 37
        entry.place(x=0, y=39, width=262, height=40)
        return entry

    def __set_search_btn(self):
        button = ThemeButton(self.parent, "Theme.entry_bg", "Theme.entry_highlight_bg",
                             foreground="Theme.main_fg")
        button.config_img(path.abspath(r"Data\ico\搜索.png"))
        button.place(x=1, y=40, height=38, width=38)
        return button

    def __set_open_new_folder_btn(self):
        button = ThemeButton(self.parent, text="打开文件夹", font=("微软雅黑", 16, "bold"))
        button.place(x=0, y=0, height=39, width=131)
        return button

    def __set_open_new_file_btn(self):
        button = ThemeButton(self.parent, text="打开图片", font=("微软雅黑", 16, "bold"))
        button.place(x=131, y=0, height=39, width=131)
        return button

    def __set_tree_view(self):
        width = 264
        height = 424
        tree_view = FileTreeView(self.parent, width, height)
        tree_view.place(x=-2, y=77, width=width, height=height)
        return tree_view

    def __set_export_btn(self):
        button = ThemeButton(self.parent, text="导出文件", font=("微软雅黑", 16, "bold"))
        button.place(x=529, y=39, width=131, height=39)
        return button

    def __set_execute_btn(self):
        button = ThemeButton(self.parent, text="立刻处理", font=("微软雅黑", 16, "bold"))
        button.place(x=405, y=39, width=131, height=39)
        return button

    def __set_export_file_tip(self):
        label = ThemeLabel(self.parent, text="文件导出路径:", font=("微软雅黑", 16, "bold"))
        label.place(x=267, y=3, width=131)
        return label

    def __set_choose_export_folder_btn(self):
        button = PushButton(self.parent, text="选择文件夹", font=("华文楷体", 13, "bold"),
                            bg_cite="Theme.button_bg", relief="flat")
        button.place(x=660, y=3, height=36, width=100)
        return button

    def __set_export_entry(self):
        entry = ThemeEntry(self.parent, font=("微软雅黑", 13))
        entry.place(x=405, y=3, width=255, height=36)
        return entry

    def __set_toning_canvas(self):
        canvas = ToningCanvas(self.parent, colours=["#FFFFFF", "#000000", "#FF0000", "#00FF00",
                                                    "#0000FF", "#FFFF00", "#FFA500", "#9B30FF"])
        canvas.place(x=660, y=42, height=35, width=230)
        return canvas

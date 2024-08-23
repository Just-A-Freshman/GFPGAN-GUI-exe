from CropFrameGUI import CropFrame
from CropFrameCore import CropCore
from Config import Theme, Init
from SharedDatabase import SharedVariable
from tkinter import filedialog, TclError, messagebox
from FileManager import FileJudgement, FileOperation
from os import path


class CropControl(CropFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.search_manager = SearchManage(self.tree_view, self.search_entry)
        self.crop_core = CropCore(self)
        self.bind_widget()
        self.link_variable()
        self.load_init_data()

    def bind_widget(self):
        self.search_btn.config_img(path.abspath(Theme.search_ico))
        self.redo_btn.config_command(self.main_canvas.redo)
        self.undo_btn.config_command(self.main_canvas.undo)
        self.execute_btn.config_command(self.crop_core.directly_add_to_task)
        self.export_btn.config_command(self.crop_core.export)
        self.open_folder_btn.config_command(self.open_folder)
        self.open_file_btn.config_command(self.open_img_file)
        self.choose_export_folder_btn.config(command=self.choose_folder)
        self.search_entry.bind("<Return>", self.search_manager.search)
        self.tree_view.bind("<<TreeviewSelect>>", self.preview)

    def load_init_data(self):
        self.export_entry.insert(0, Init.export_path)
        if path.isdir(Init.open_folder):
            self.tree_view.build_catalog_tree(Init.open_folder)

    def update_widget_color(self):
        widgets = (self.main_canvas, self.undo_btn, self.redo_btn, self.tree_view, self.search_entry,
                   self.search_btn, self.open_file_btn, self.open_folder_btn, self.execute_btn,
                   self.export_btn, self.export_entry, self.choose_export_folder_btn, self.tip_label1,
                   self.toning_canvas, self.tree_view)
        for widget in widgets:
            widget.config(widget.get_dynamic_style)
        self.search_btn.config_img(path.abspath(Theme.search_ico))

    def link_variable(self):
        self.tree_view.outer_link = self.delete_file
        SharedVariable.save_setting = self.save_current_setting

    def open_folder(self, _):
        folder = filedialog.askdirectory()
        if folder:
            self.tree_view.build_catalog_tree(folder)

    def open_img_file(self, _):
        img_file = FileJudgement.ask_open_img()
        if not img_file:
            return
        self.main_canvas.change_img(img_file)
        self.main_canvas.bind_palette()

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.export_entry.delete(0, 'end')
            self.export_entry.insert(0, folder)

    def preview(self, _):
        item = self.tree_view.selection()
        if len(item) == 0:
            return
        base_name = self.tree_view.get_selected_abs_path(item[0])
        if not path.exists(base_name):
            messagebox.showinfo("提示", "该文件已被移动或删除!")
            self.tree_view.delete(item)
        elif path.isdir(base_name):
            if self.main_canvas.get_current_img_path == "":
                return
            self.main_canvas.show_default_img()
        else:
            self.main_canvas.change_img(base_name)
            self.main_canvas.bind_palette()

    def delete_file(self):
        item = self.tree_view.selection()[0]
        file_path = self.tree_view.get_selected_abs_path(item)
        is_delete = FileOperation.remove_file(file_path)
        if is_delete:
            self.tree_view.delete(item)
            self.main_canvas.show_default_img()

    def save_current_setting(self):
        Init.export_path = self.export_entry.get()
        Init.open_folder = self.tree_view.item(self.tree_view.get_children(''))["text"]
        Init.save_current_init()


class SearchManage(object):
    def __init__(self, tree_view, search_entry):
        self.tree_view = tree_view
        self.search_entry = search_entry
        self.__before_search = ""
        self.__search_results = []
        self.__current_pos = 0

    def goto_result(self):
        try:
            item = self.__search_results[self.__current_pos]
            self.tree_view.focus(item)
            self.tree_view.selection_set(item)
            self.tree_view.see(item)
        except (TclError, IndexError):
            self.__before_search = ""

    def search(self, _):
        key = self.search_entry.get()
        if key == "":
            return
        if key == self.__before_search:
            self.__current_pos += 1
            if self.__current_pos == len(self.__search_results):
                self.__current_pos = 0
            self.goto_result()
        else:
            self.__search_results = self.tree_view.search_node(key)
            self.__before_search = key
            self.__current_pos = 0
            self.goto_result()

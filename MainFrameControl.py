from ImageApp import ImageApp
from threading import Thread
from FileManager import FileJudgement, SpgManager
from tkinter_extension.Widget.Command import FileCommand
from SharedDatabase import SendData, SharedVariable
from os import path, startfile
from Config import Theme, Init
from tkinter import filedialog, messagebox
from ThemeWidget import ImageLabel
from MainFrameGUI import MainFrame
from time import time, sleep


class GuiControl(MainFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.page_manager = PageManager(self)
        self.executor = self.initialize_executor()
        self.__before_call_time = 0          # 这个变量用于专门限制refresh按钮被高频次点击导致崩溃
        Thread(target=self.initialize).start()

    def initialize(self):
        self.load_init_data()
        self.initialize_fixed_variables()
        self.bind_command()
        self.bind_event()

    def update_widget_color(self):
        # first part
        ImageLabel.overwrite = False
        labels = (self.label1, self.label2, self.label3, self.label4, self.label5, self.label6)
        flat_btn1 = (
            self.left_btn, self.right_btn, self.task_clear_btn, self.remove_task_btn,
            self.refresh_task_btn, self.up_task_btn, self.down_task_btn
        )
        flat_btn2 = (self.open_folder1, self.open_folder2, self.choose_folder1, self.choose_folder2)
        entry1 = (self.infile_path_entry, self.outfile_path_entry, )
        readonly_entry = (self.orig_img_info_entry, self.processed_img_info_entry)
        scrollbars = (self.listbox_h_scrollbar, self.listbox_v_scrollbar)
        others = (self.img_label1, self.img_label2)

        for label in labels:
            label.config(**Theme.style_dict["Label"])
        for btn in flat_btn1:
            btn.config(**Theme.style_dict["FlatButton-1"])
        for btn in flat_btn2:
            btn.config(**Theme.style_dict["FlatButton-2"])
        for entry in entry1:
            entry.config(**Theme.style_dict["Entry-1"])
        for entry in readonly_entry:
            entry.config(**Theme.style_dict["ReadonlyEntry"])
        for scrollbar in scrollbars:
            scrollbar.config(**Theme.style_dict["Scrollbar"])
        for widget in others:
            widget.config(widget.get_dynamic_style)
        self.tip_entry.config(**Theme.style_dict["Entry-2"])
        self.execute_btn.config(**Theme.style_dict["FlatButton-3"])
        self.progressbar.config(**Theme.style_dict["ProgressBar"])
        self.task_list.config(**Theme.style_dict["Listbox"])
        # second part
        ImageLabel.overwrite = True
        self.parent.config(bg=Theme.win_bg)
        self.config_ttk_style()
        self.up_scale_slider.config(
            bg=Theme.win_bg, foreground=Theme.main_fg,
            activebackground=Theme.win_bg, troughcolor=Theme.scrollbar_bg
        )

    def bind_command(self):
        commands = (self.task_list.up_task_list, self.task_list.down_task_list,
                    self.task_list.delete_current_select, self.task_list.delete_all, self.load_folder_to_task_list)
        theme_buttons = (self.up_task_btn, self.down_task_btn, self.remove_task_btn,
                         self.task_clear_btn, self.refresh_task_btn)
        for button, command in zip(theme_buttons, commands):
            button.config(command=command)
        self.left_btn.config(command=lambda _: self.page_manager.turn_left())
        self.right_btn.config(command=lambda _: self.page_manager.turn_right())
        self.choose_folder1.config(command=lambda _: self.choose_folder(True))
        self.choose_folder2.config(command=lambda _: self.choose_folder(False))
        self.open_folder1.config(command=lambda _: self.start_folder(True))
        self.open_folder2.config(command=lambda _: self.start_folder(False))
        self.listbox_v_scrollbar.config(command=self.task_list.yview)
        self.listbox_h_scrollbar.config(command=self.task_list.xview)
        self.task_list.configure(yscrollcommand=self.listbox_v_scrollbar.set)
        self.task_list.configure(xscrollcommand=self.listbox_h_scrollbar.set)
        self.execute_btn.config(command=self.main)

    def bind_event(self):
        self.task_list.bind("<Double-Button-1>", lambda _: self.task_list.open_file(_, SendData.infile))
        self.img_label1.bind("<Double-Button-1>", self.start_file)
        self.img_label2.bind("<Double-Button-1>", self.start_file)
        self.img_label1.bind('<Button-3>', self.create_menu)
        self.img_label2.bind('<Button-3>', self.create_menu)

    def load_init_data(self):
        self.infile_path_entry.insert(0, Init.infile_path)
        self.outfile_path_entry.insert(0, Init.outfile_path)
        if path.exists(Init.infile_path):
            SendData.refresh_file_id(Init.infile_path, cite="infile")
            self.load_folder_to_task_list(0)
        if path.exists(Init.outfile_path):
            SendData.refresh_file_id(Init.outfile_path, cite="outfile")

    def create_menu(self, event):
        img_path = event.widget.cget("textvariable")
        i = 1 if isinstance(img_path, int) else 0
        states = ("active", "disabled")
        state = states[i]
        self.file_menu.create_menu(event, img_path, state)

    def load_folder_to_task_list(self, _):
        if time() - self.__before_call_time < 1:
            self.__before_call_time = time()
            return
        if not path.isdir(SendData.infile):
            return
        self.task_list.load_folder(0, SendData.infile)
        self.__before_call_time = time()

    def choose_folder(self, is_infile: bool):
        entry = self.infile_path_entry if is_infile else self.outfile_path_entry
        initial_dir = entry.get()
        folder_selected = filedialog.askdirectory(initialdir=initial_dir)
        if not folder_selected:
            return
        entry.delete(0, 'end')
        entry.insert(0, folder_selected)
        if is_infile:
            SendData.refresh_file_id(folder_selected, cite="infile")
            self.task_list.load_folder(0, folder_selected)
        else:
            SendData.refresh_file_id(self.outfile_path_entry.get(), cite="outfile")

    def start_file(self, event):
        file_path = self.img_label1.cget("textvariable") if event.x_root < 750 \
            else self.img_label2.cget("textvariable")
        if isinstance(file_path, int):
            return
        Thread(target=FileCommand.FileOperation.start_file(file_path)).start()

    def start_folder(self, flag):
        folder_path = self.infile_path_entry.get() if flag else self.outfile_path_entry.get()
        if folder_path == '':
            return messagebox.showinfo('提示', '没有文件夹可以打开!')
        if not path.isdir(folder_path):
            return messagebox.showerror('错误', '文件夹路径错误, \n无法打开!')
        Thread(target=startfile, args=(folder_path, )).start()

    def load_single_picture(self, img_path=None):
        img_path = FileJudgement.ask_open_img() if img_path is None else img_path
        if not img_path:
            return
        photo = ImageApp.create_thumbnail(img_path)
        self.change_img((photo, img_path))
        self.img_label2.config(**self.img_label2.get_dynamic_style)
        self.infile_path_entry.delete(0, 'end')
        self.infile_path_entry.insert(0, path.dirname(img_path))
        self.task_list.delete(0, 'end')
        self.task_list.insert(0, path.basename(img_path))
        SendData.refresh_file_id(path.dirname(img_path), cite="infile")

    def load_spg_file(self):
        file_types = (("SPG files", "*.spg"),)
        spg_file = filedialog.askopenfilename(filetypes=file_types)
        if not spg_file:
            return
        result = SpgManager.decompress_img(spg_file)
        if result == "":
            return messagebox.showerror("错误", "无法识别该spg文件!")
        self.load_single_picture(result)
        self.task_list.delete(0, 'end')
        self.task_list.insert(0, path.basename(spg_file))

    def change_img(self, orig_tuple: tuple, processed_tuple: tuple = ()):
        # You should make sure the orig_tuple should contain two elements, ImageTk obj and img path
        orig_img, orig_img_path = orig_tuple
        if path.isfile(orig_img_path):
            self.img_label1.config(image=orig_img, textvariable=orig_img_path)
            self.orig_img_info_entry.refresh(
                f"{path.basename(orig_img_path)}—{ImageApp.get_img_size(orig_img_path)}"
            )
            self.img_label1.image = orig_img
        else:
            self.img_label1.config(self.img_label1.get_dynamic_style)
        if len(processed_tuple) == 0:
            return
        processed_img, processed_img_path = processed_tuple
        if path.isfile(processed_img_path):
            self.img_label2.config(image=processed_img, textvariable=processed_img_path)
            self.processed_img_info_entry.refresh(f"{ImageApp.get_img_size(processed_img_path)}")
            self.img_label2.image = processed_img
        else:
            self.img_label2.config(self.img_label2.get_dynamic_style)
        return True if path.isfile(orig_img_path) or path.isfile(processed_img_path) else False

    def overwrite_to_show_label(self, content):
        self.tip_entry.delete(0, 'end')
        self.tip_entry.insert(0, content)
        self.tip_entry.icursor('end')
        self.tip_entry.xview_moveto(1)

    def save_current_setting(self):
        Init.infile_path = self.infile_path_entry.get()
        Init.outfile_path = self.outfile_path_entry.get()
        SharedVariable.save_setting()

    def send_task(self):
        if self.task_list.size() == 0:
            return
        task = self.task_list.get(0)
        while not ImageApp.is_real_img(path.join(SendData.infile, task)):
            self.overwrite_to_show_label(f"包含中文/非图片:{task}")
            self.task_list.delete(0)
            task = self.task_list.get(0)
            sleep(1)
        SendData.extension = self.extension_combobox.get()
        SendData.scale = self.up_scale_slider.get()
        SendData.write_in_task_list(self.task_list.get(0))
        self.task_list.delete(0)

    def clear_all(self):
        self.img_label1.config(self.img_label1.get_dynamic_style)
        self.img_label2.config(self.img_label2.get_dynamic_style)
        self.infile_path_entry.delete(0, 'end')
        self.outfile_path_entry.delete(0, 'end')
        self.orig_img_info_entry.refresh("")
        self.processed_img_info_entry.refresh("")
        self.task_list.delete_all(0, ask_cancel=False)

    def initialize_executor(self):
        from MainFrameCore import ExecuteCommand
        executor = ExecuteCommand(self.page_manager, self)
        return executor

    def initialize_fixed_variables(self):
        SendData.initialize_all_table()
        SharedVariable.task_list = self.task_list
        SharedVariable.execute_entry = self.main

    def main(self, _):
        if FileJudgement.is_folder_name_error(
                self.infile_path_entry.get(),
                self.outfile_path_entry.get(),
                extra_title="来自人脸超分辨率的"
        ):
            return False
        SharedVariable.working = True
        self.executor.launch_main_thread()
        return True


class PageManager:
    from functools import lru_cache

    def __init__(self, control):
        self.control: GuiControl = control
        self.finish_signal = False
        self.__current_page = 0
        self.__max_page = 0

    def turn_page(self, left):
        if left:
            if self.__current_page in [0, 1]:
                return messagebox.showinfo("提示", "当前已是第一页!")
            self.__current_page -= 1
        else:
            if self.__current_page == self.__max_page:
                return messagebox.showinfo("提示", "当前已是最后一页!")
            self.__current_page += 1
        orig_tuple, processed_tuple = self.get_img_info(self.__current_page)
        result = self.control.change_img(orig_tuple, processed_tuple)
        if not result:
            return self.turn_left() if left else self.turn_right()
        self.pre_read()

    def turn_left(self):
        self.turn_page(left=True)

    def turn_right(self):
        self.turn_page(left=False)

    @lru_cache(maxsize=15)
    def get_img_info(self, current_page):
        infile_path, outfile_path = SendData.select_finish_deal_img(current_page)
        orig_img = ImageApp.create_thumbnail(infile_path)
        processed_img = ImageApp.create_thumbnail(outfile_path)
        return (orig_img, infile_path), (processed_img, outfile_path)

    def dynamic_show_img_to_label(self):
        if not self.finish_signal:
            return
        self.finish_signal = False
        self.__max_page += 1
        orig_tuple, processed_tuple = self.get_img_info(self.__max_page)
        self.control.change_img(orig_tuple, processed_tuple)
        self.__current_page = self.__max_page

    def pre_read(self):
        for i in range(self.__current_page - 3, self.__current_page + 3):
            if 0 < i < self.__max_page + 1:
                Thread(target=self.get_img_info, args=(i, )).start()

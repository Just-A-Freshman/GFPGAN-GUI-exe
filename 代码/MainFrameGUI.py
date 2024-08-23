from ThemeWidget import (ThemeButton, ThemeLabel, ThemeEntry, ReadOnlyEntry,
                         PushButton, ThemeListbox, ImageLabel, Label,
                         StyleConfig, MyProgressbar)
from tkinter import (Frame, IntVar, Scale, HORIZONTAL)
from tkinter.ttk import Combobox
from Config import Theme


class MainFrame(object):
    def __init__(self, parent):
        self.parent: Frame = parent
        self.slider_val = IntVar(value=1)

        # style_config
        self.style_config = self.__style_config()

        # place all label
        self.label1 = self.__set_tip_label1()
        self.label2 = self.__set_tip_label2()
        self.label3 = self.__set_tip_label3()
        self.label4 = self.__set_tip_label4()
        self.label5 = self.__set_tip_label5()
        self.label6 = self.__set_tip_label6()
        self.img_label1 = self.__set_img_label1()
        self.img_label2 = self.__set_img_label2()

        # place all input widget
        self.infile_path_entry = self.__set_infile_path_entry()
        self.outfile_path_entry = self.__set_outfile_path_entry()
        self.extension_combobox = self.__set_combobox()
        self.up_scale_slider = self.__set_up_scale_slider()

        # set all output widget
        self.tip_entry = self.__set_tip_entry()
        self.orig_img_info_entry = self.__orig_img_info_entry()
        self.processed_img_info_entry = self.__processed_img_info_entry()
        self.progressbar = self.__set_progressbar()
        self.task_list = self.__set_task_list()

        # place all button
        self.open_folder1 = self.__set_open_folder_btb1()
        self.open_folder2 = self.__set_open_folder_btn2()
        self.choose_folder1 = self.__set_choose_folder_btn1()
        self.choose_folder2 = self.__set_choose_folder_btn2()
        self.left_btn = self.__set_left_btn()
        self.right_btn = self.__set_right_btn()
        self.task_clear_btn = self.__set_clear_btn()
        self.remove_task_btn = self.__set_remove_task()
        self.refresh_task_btn = self.__set_refresh_task()
        self.up_task_btn = self.__up_task_btn()
        self.down_task_btn = self.__down_task_btn()
        self.execute_btn = self.__set_execute_btn()

        # place the decorate separator
        self.v_separator = self.__set_vertical_separator()
        self.h_seperator = self.__set_horizontal_separator()

    def __set_tip_label1(self):
        label = ThemeLabel(self.parent, text='原图', font=('微软雅黑', 17))
        label.place(x=10, y=242, height=30)
        return label

    def __set_tip_label2(self):
        label = ThemeLabel(self.parent, text='效果图', font=('微软雅黑', 17))
        label.place(x=455, y=242, height=30)
        return label

    def __set_tip_label3(self):
        label = ThemeLabel(self.parent, text='输入路径:', font=('微软雅黑', 15))
        label.place(x=10, y=290)
        return label

    def __set_tip_label4(self):
        label = ThemeLabel(self.parent, text='输出路径:', font=('微软雅黑', 15))
        label.place(x=10, y=340)
        return label

    def __set_tip_label5(self):
        label = ThemeLabel(self.parent, text='图片缩放:', font=('微软雅黑', 15))
        label.place(x=220, y=392)
        return label

    def __set_tip_label6(self):
        label = ThemeLabel(self.parent, text='输出格式:', font=('微软雅黑', 15))
        label.place(x=10, y=392)
        return label

    def __set_open_folder_btb1(self):
        button = PushButton(self.parent, text=">>", bg_cite="Theme.button_bg",
                            font=('宋体', 18, 'bold'), relief="flat")
        button.place(x=390, y=290, height=30, width=35)
        return button

    def __set_open_folder_btn2(self):
        button = PushButton(self.parent, text=">>", bg_cite="Theme.button_bg",
                            font=('宋体', 18, 'bold'), relief="flat")
        button.place(x=390, y=340, height=30, width=35)
        return button

    def __set_left_btn(self):
        button = PushButton(self.parent, text='\u25C0', bg_cite="Theme.win_bg",
                            fg_cite="Theme.button_fg", font=('宋体', 30, 'bold'), relief="flat")
        button.config_enter_style()
        button.place(x=350, y=242, height=31, width=40)
        return button

    def __set_right_btn(self):
        button = PushButton(self.parent, text='\u25B6', bg_cite="Theme.win_bg",
                            fg_cite="Theme.button_fg", font=('宋体', 30, 'bold'), relief="flat")
        button.config_enter_style()
        button.place(x=390, y=242, height=31, width=40)
        return button

    def __set_choose_folder_btn1(self):
        button = PushButton(self.parent, text='+', bg_cite="Theme.button_bg",
                            font=("宋体", 30), relief="flat")
        button.place(x=350, y=290, width=39, height=30)
        return button

    def __set_choose_folder_btn2(self):
        button = PushButton(self.parent, text='+', bg_cite="Theme.button_bg",
                            font=("宋体", 30), relief="flat")
        button.place(x=350, y=340, width=39, height=30)
        return button

    def __set_clear_btn(self):
        button = ThemeButton(self.parent, text="清空", font=("微软雅黑", 16, "bold"))
        button.place(x=821, y=304, height=48, width=79)
        return button

    def __set_remove_task(self):
        button = ThemeButton(self.parent, text="移除", font=("微软雅黑", 16, "bold"))
        button.place(x=743, y=304, height=48, width=78)
        return button

    def __set_refresh_task(self):
        button = ThemeButton(self.parent, text="重载任务", font=("微软雅黑", 16, "bold"))
        button.place(x=743, y=352, height=48, width=157)
        return button

    def __up_task_btn(self):
        button = ThemeButton(self.parent, text="上移任务", font=("微软雅黑", 16, "bold"))
        button.place(x=743, y=400, height=50, width=157)
        return button

    def __down_task_btn(self):
        button = ThemeButton(self.parent, text="下移任务", font=("微软雅黑", 16, "bold"))
        button.place(x=743, y=450, height=50, width=157)
        return button

    def __set_execute_btn(self):
        button = PushButton(self.parent, text='开 始 处 理', font=('微软雅黑', 18),
                            bg_cite="Theme.execute_btn_bg", fg_cite="Theme.execute_btn_fg")
        button.place(x=135, y=440, width=180, height=55)
        return button

    def __set_infile_path_entry(self):
        entry = ThemeEntry(self.parent, font=("微软雅黑", 12))
        entry.place(x=105, y=290, height=30, width=246)
        return entry

    def __set_outfile_path_entry(self):
        entry = ThemeEntry(self.parent, font=("微软雅黑", 12))
        entry.place(x=105, y=340, height=30, width=246)
        return entry

    def __set_tip_entry(self):
        entry = ThemeEntry(self.parent, font=("微软雅黑", 12), bg_cite="Theme.win_bg",
                           border=False, start_pos=3, highlightcolor="#595959")
        entry.place(x=451, y=274, width=281, height=30)
        return entry

    def __orig_img_info_entry(self):
        entry = ReadOnlyEntry(self.parent, font=("微软雅黑", 14), bg_cite="Theme.win_bg")
        entry.place(x=110, y=243, width=240, height=31)
        return entry

    def __processed_img_info_entry(self):
        entry = ReadOnlyEntry(self.parent, font=("微软雅黑", 14), bg_cite="Theme.win_bg")
        entry.place(x=640, y=243, height=30)
        return entry

    def __set_task_list(self):
        listbox = ThemeListbox(self.parent)
        listbox.place(x=450, y=304, width=294, height=197)
        return listbox

    def __set_progressbar(self):
        progressbar = MyProgressbar(self.parent, background=Theme.scrollbar_bg, borderwidth=1,
                                    highlightcolor=Theme.scrollbar_highlight_bg, bar_bg=Theme.progressbar_color)
        progressbar.place(x=731, y=275, width=170, height=29)
        return progressbar

    def __set_combobox(self):
        extension_combobox = Combobox(self.parent, values=['auto', 'png', 'jpg', 'jpeg'],
                                      style="customer.TCombobox")
        extension_combobox.insert('end', 'auto')
        extension_combobox.config(state='readonly', font=('微软雅黑', 13))
        extension_combobox.place(x=105, y=392, width=65, height=32)
        return extension_combobox

    def __set_up_scale_slider(self):
        slider = Scale(self.parent, from_=1, to=10, orient=HORIZONTAL, width=25, borderwidth=2,
                       highlightthickness=0, relief='flat', variable=self.slider_val,
                       bg=Theme.win_bg, foreground=Theme.main_fg, activebackground=Theme.win_bg,
                       troughcolor=Theme.scrollbar_bg)
        slider.place(x=311, y=370, width=120)
        return slider

    def __set_img_label1(self):
        label = ImageLabel(self.parent, 0)
        label.place(x=0, y=-3, width=450, height=246)
        return label

    def __set_img_label2(self):
        label = ImageLabel(self.parent, 1)
        label.place(x=450, y=-3, width=450, height=246)
        return label

    def __set_vertical_separator(self):
        separator = Label(self.parent, highlightthickness=4, highlightbackground='#595959')
        separator.place(x=448, y=0, width=4, height=600)
        return separator

    def __set_horizontal_separator(self):
        separator1 = Label(self.parent, highlightthickness=4, highlightbackground='#595959')
        separator1.place(x=0, y=273, width=900, height=2)
        separator2 = Label(self.parent, highlightthickness=4, highlightbackground='#595959')
        separator2.place(x=0, y=242, width=900, height=2)
        separator3 = Label(self.parent, highlightthickness=1, highlightbackground=Theme.scrollbar_bg)
        separator3.place(x=731, y=304, width=12, height=1)
        return separator1, separator2, separator3

    @staticmethod
    def __style_config():
        style = StyleConfig()
        return style

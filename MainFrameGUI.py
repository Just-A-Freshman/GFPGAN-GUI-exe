from ThemeWidget import TaskListbox, ImageLabel
from tkinter import (Frame, Label, IntVar, Scale, HORIZONTAL)
from tkinter_extension.Widget.Button import FlatButton
from tkinter_extension.Widget.Entry import CustomEntry, ReadOnlyEntry
from tkinter_extension.Widget.ProgressBar import Progressbar
from tkinter_extension.Widget.ContextMenu import FileMenu
from tkinter_extension.Widget.Scrollbar import BorderlessScrollbar
from tkinter.ttk import Combobox, Style
from Config import Theme


class MainFrame(object):
    def __init__(self, parent):
        self.parent: Frame = parent
        self.slider_val = IntVar(value=1)

        # style some ttk style, like the Combobox
        self.config_ttk_style()

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

        # others: separator、file_menu、scrollbar, progressbar
        self.file_menu = self.__set_context_menu()
        self.listbox_v_scrollbar = self.__set_listbox_v_scrollbar()
        self.listbox_h_scrollbar = self.__set_listbox_h_scrollbar()
        self.v_separator = self.__set_vertical_separator()
        self.h_seperator = self.__set_horizontal_separator()
        self.progressbar = self.__set_progressbar()

    def __set_tip_label1(self):
        label = Label(self.parent, text='原图', font=Theme.font_box[5], **Theme.style_dict["Label"])
        label.place(x=10, y=242, height=30)
        return label

    def __set_tip_label2(self):
        label = Label(self.parent, text='效果图', font=Theme.font_box[5], **Theme.style_dict["Label"])
        label.place(x=455, y=242, height=30)
        return label

    def __set_tip_label3(self):
        label = Label(self.parent, text='输入路径:', font=Theme.font_box[3], **Theme.style_dict["Label"])
        label.place(x=10, y=290)
        return label

    def __set_tip_label4(self):
        label = Label(self.parent, text='输出路径:', font=Theme.font_box[3], **Theme.style_dict["Label"])
        label.place(x=10, y=340)
        return label

    def __set_tip_label5(self):
        label = Label(self.parent, text='图片缩放:', font=Theme.font_box[3], **Theme.style_dict["Label"])
        label.place(x=220, y=392)
        return label

    def __set_tip_label6(self):
        label = Label(self.parent, text='输出格式:', font=Theme.font_box[3], **Theme.style_dict["Label"])
        label.place(x=10, y=392)
        return label

    def __set_open_folder_btb1(self):
        button = FlatButton(self.parent, text=">>", font=Theme.font_box[7],
                            **Theme.style_dict["FlatButton-2"])
        button.place(x=390, y=290, height=30, width=35)
        return button

    def __set_open_folder_btn2(self):
        button = FlatButton(self.parent, text=">>", font=Theme.font_box[7],
                            **Theme.style_dict["FlatButton-2"])
        button.place(x=390, y=340, height=30, width=35)
        return button

    def __set_left_btn(self):
        button = FlatButton(self.parent, text='\u25C0', font=Theme.font_box[8],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=350, y=242, height=31, width=40)
        return button

    def __set_right_btn(self):
        button = FlatButton(self.parent, text='\u25B6', font=Theme.font_box[8],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=390, y=242, height=31, width=40)
        return button

    def __set_choose_folder_btn1(self):
        button = FlatButton(self.parent, text='+', font=Theme.font_box[8],
                            **Theme.style_dict["FlatButton-2"])
        button.place(x=350, y=290, width=39, height=30)
        return button

    def __set_choose_folder_btn2(self):
        button = FlatButton(self.parent, text='+', font=Theme.font_box[8],
                            **Theme.style_dict["FlatButton-2"])
        button.place(x=350, y=340, width=39, height=30)
        return button

    def __set_clear_btn(self):
        button = FlatButton(self.parent, text="清空", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=821, y=304, height=48, width=79)
        return button

    def __set_remove_task(self):
        button = FlatButton(self.parent, text="移除", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=743, y=304, height=48, width=78)
        return button

    def __set_refresh_task(self):
        button = FlatButton(self.parent, text="重载任务", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=743, y=352, height=48, width=157)
        return button

    def __up_task_btn(self):
        button = FlatButton(self.parent, text="上移任务", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=743, y=400, height=50, width=157)
        return button

    def __down_task_btn(self):
        button = FlatButton(self.parent, text="下移任务", font=Theme.font_box[4],
                            **Theme.style_dict["FlatButton-1"])
        button.place(x=743, y=450, height=50, width=157)
        return button

    def __set_execute_btn(self):
        button = FlatButton(self.parent, text='开 始 处 理', font=Theme.font_box[6],
                            **Theme.style_dict["FlatButton-3"])
        button.place(x=135, y=440, width=180, height=55)
        return button

    def __set_infile_path_entry(self):
        entry = CustomEntry(self.parent, font=Theme.font_box[0], **Theme.style_dict["Entry-1"])
        entry.place(x=105, y=290, height=30, width=246)
        return entry

    def __set_outfile_path_entry(self):
        entry = CustomEntry(self.parent, font=Theme.font_box[0], **Theme.style_dict["Entry-1"])
        entry.place(x=105, y=340, height=30, width=246)
        return entry

    def __set_tip_entry(self):
        entry = CustomEntry(self.parent, font=Theme.font_box[0], border=False, start_pos=3,
                            highlightcolor="#595959", **Theme.style_dict["Entry-2"])
        entry.place(x=451, y=274, width=281, height=31)
        return entry

    def __orig_img_info_entry(self):
        entry = ReadOnlyEntry(self.parent, font=Theme.font_box[2], **Theme.style_dict["ReadonlyEntry"])
        entry.place(x=110, y=243, width=240, height=31)
        return entry

    def __processed_img_info_entry(self):
        entry = ReadOnlyEntry(self.parent, font=Theme.font_box[2], **Theme.style_dict["ReadonlyEntry"])
        entry.place(x=640, y=243, height=30)
        return entry

    def __set_task_list(self):
        listbox = TaskListbox(
            self.parent, font=Theme.font_box[1], relief="flat", borderwidth=-1,
            **Theme.style_dict["Listbox"]
        )
        listbox.place(x=450, y=304, width=284, height=184)
        return listbox

    def __set_listbox_v_scrollbar(self):
        scrollbar = BorderlessScrollbar(self.parent, cursor="hand2", **Theme.style_dict["Scrollbar"])
        scrollbar.place(x=730, y=303, height=198)
        return scrollbar

    def __set_listbox_h_scrollbar(self):
        scrollbar = BorderlessScrollbar(
            self.parent, cursor="hand2", orient="horizontal",
            **Theme.style_dict["Scrollbar"],
        )
        scrollbar.place(x=451, y=487, width=293)
        return scrollbar

    def __set_progressbar(self):
        progressbar = Progressbar(self.parent, borderwidth=1, **Theme.style_dict["ProgressBar"])
        progressbar.place(x=731, y=275, width=170, height=29)
        return progressbar

    def __set_combobox(self):
        extension_combobox = Combobox(
            self.parent, values=['auto', 'png', 'jpg', 'jpeg'], style="customer.TCombobox"
        )
        extension_combobox.insert('end', 'auto')
        extension_combobox.config(state='readonly', font=Theme.font_box[1])
        extension_combobox.place(x=105, y=392, width=65, height=32)
        return extension_combobox

    def __set_up_scale_slider(self):
        slider = Scale(
            self.parent, from_=1, to=10, orient=HORIZONTAL, width=25, borderwidth=2,
            highlightthickness=0, relief='flat', variable=self.slider_val,
            **Theme.style_dict["Scale"]
        )
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

    def __set_context_menu(self):
        file_menu = FileMenu(self.parent, font=Theme.font_box[2])
        return file_menu

    def __set_vertical_separator(self):
        separator = Label(self.parent, highlightthickness=4, highlightbackground='#595959')
        separator.place(x=448, y=0, width=4, height=600)
        return separator

    def __set_horizontal_separator(self):
        separator1 = Label(self.parent, highlightthickness=4, highlightbackground='#595959')
        separator1.place(x=0, y=273, width=900, height=2)
        separator2 = Label(self.parent, highlightthickness=4, highlightbackground='#595959')
        separator2.place(x=0, y=242, width=900, height=2)
        return separator1, separator2

    @staticmethod
    def config_ttk_style():
        style = Style()
        style.configure("customer.TCombobox", **Theme.style_dict["Combobox"])
        style.map("TCombobox", **Theme.style_dict["TCombobox_map"])

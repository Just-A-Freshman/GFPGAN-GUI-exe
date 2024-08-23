from Config import Theme
from tkinter import (Label, Entry, Button, Listbox, Canvas, Menu, Frame,
                     font as tk_font, TclError, messagebox, PhotoImage)
from tkinter.ttk import Scrollbar, Treeview, Style
from ImageApp import Image, ImageTk, ImageApp
from FileManager import FileJudgement, FileOperation, SpgManager
from os import path, scandir
from threading import Thread
import re


# set some global property
global_style = Style()
global_style.theme_use("clam")

# load global image resource
folder_img = ImageTk.PhotoImage(file="Data/ico/folder.png")
img_file = ImageTk.PhotoImage(file="Data/ico/img.png")
copy_ico = PhotoImage(file=r"Data/ico/copy.png")
open_ico = PhotoImage(file=r"Data/ico/open.png")
copy_path_ico = PhotoImage(file=r"Data/ico/copy_path.png")
delete_ico = PhotoImage(file=r"Data/ico/delete.png")


class StyleConfig:
    config_scrollbar = ("Vertical.TScrollbar", "Horizontal.TScrollbar")
    config_combobox = "customer.TCombobox"
    scrollbar_style = {
        "gripcount": 0,
        "arrowcolor": "white"
    }

    def __init__(self):
        for config_obj in StyleConfig.config_scrollbar:
            global_style.configure(config_obj, **StyleConfig.scrollbar_style)
        self.re_config()

    @classmethod
    def re_config(cls):
        for config_obj in cls.config_scrollbar:
            global_style.configure(
                config_obj,
                background=Theme.scrollbar_bg,
                troughcolor=Theme.win_bg,
                bordercolor=Theme.win_bg,
                lightcolor=Theme.scrollbar_bg,
                darkcolor=Theme.scrollbar_bg,
            )
        global_style.map(
            "TScrollbar",
            background=[('active', Theme.scrollbar_highlight_bg)]
        )
        global_style.configure(
            cls.config_combobox,
            arrowcolor=Theme.main_fg,
            foreground=Theme.main_fg,
            background=Theme.scrollbar_bg,
            lightcolor=Theme.scrollbar_bg,
            darkcolor=Theme.scrollbar_bg,
            dropdownbackground='red'
        )
        global_style.map(
            "TCombobox",
            background=[('active', Theme.scrollbar_highlight_bg)],
            fieldbackground=[('readonly', Theme.scrollbar_bg)],
        )


class MyProgressbar:
    def __init__(self, parent, borderwidth=2, bar_bg="orange", background="white",
                 highlightcolor="black"):
        self.parent = parent
        self.borderwidth = borderwidth
        self.highlight_color = highlightcolor
        self.bar_bg = bar_bg
        self.background = background
        self.__bar = None
        self.__step: float = 1.0
        self.__current_length = 0
        self.__start_x = 0
        self.__start_y = 0
        self.__bar_height = 0

    def place(self, x, y, width, height):
        self.__step = (width - self.borderwidth*2) / 100
        self.__start_x = x + self.borderwidth
        self.__start_y = y + self.borderwidth
        self.__bar_height = height - self.borderwidth * 2
        self.__drawing(x, y, width, height)

    def __drawing(self, x, y, width, height):
        self.border = Label(self.parent, bg=self.highlight_color)
        self.border.place(x=x, y=y, width=width, height=height)  # 进度条外框
        self.inner = Label(self.parent, bg=self.background)
        self.inner.place(
            x=self.__start_x, y=self.__start_y,
            width=width-self.borderwidth*2, height=height-self.borderwidth*2
        )
        self.__bar = Label(self.parent, bg=self.bar_bg)

    def config(self, para_dict: dict):
        for k, v in para_dict.items():
            match k:
                case 'highlightcolor': self.border.config(bg=v)
                case 'background': self.inner.config(bg=v)
                case 'bar_bg': self.__bar.config(bg=v)
                case _: continue

    def step(self, value):
        width = self.__bar.winfo_width()
        new_width = width + value * self.__step
        if new_width > self.inner.winfo_width():
            self.set(100)
        else:
            self.__bar.place(width=new_width)

    def set(self, value):
        self.__bar.place(
            x=self.__start_x, y=self.__start_y,
            width=value * self.__step, height=self.__bar_height
        )  # 进度条内部

    @property
    def get_dynamic_style(self):
        return {
            'highlightcolor': Theme.scrollbar_highlight_bg,
            'background': Theme.scrollbar_bg,
            'bar_bg': Theme.progressbar_color
        }


class ThemeButton(Label):
    def __init__(self, parent, btn_bg: str = "Theme.win_bg", enter_bg: str = "Theme.btn_enter_bg",
                 foreground: str = "Theme.button_fg", **kwargs):
        self.image = ""
        self.btn_bg = btn_bg
        self.foreground = foreground
        super().__init__(parent, **kwargs, **self.get_dynamic_style)
        self.bind('<Enter>', lambda event: self.config(bg=eval(enter_bg), cursor='hand2'))
        self.bind('<Leave>', lambda event: self.config(bg=eval(btn_bg)))
        self.bind('<ButtonRelease-1>', self.__click_handle)
        self.__command = lambda event: None

    def config_img(self, img_path):
        if not path.isfile(img_path):
            return
        img = ImageTk.PhotoImage(file=img_path)
        self.image = img
        self.config(image=img)

    def config_command(self, command):
        self.__command = command

    @property
    def get_dynamic_style(self):
        dynamic_style = {
            "bg": eval(self.btn_bg),
            "foreground": eval(self.foreground)
        }
        return dynamic_style

    def __click_handle(self, event):
        if event.widget.cget('bg') != Theme.btn_enter_bg:
            return
        self.__command(event)


class PushButton(Button):
    def __init__(self, parent, text, bg_cite: str, fg_cite: str = "Theme.switch_frame_fg", **kwargs):
        self.bg_cite = bg_cite
        self.fg_cite = fg_cite
        super().__init__(parent, text=text, **self.get_dynamic_style, **kwargs)

    @property
    def get_dynamic_style(self):
        dynamic_style = {
            "bg": eval(self.bg_cite),
            "foreground": eval(self.fg_cite),
            "activebackground": eval(self.bg_cite),
            "activeforeground": eval(self.fg_cite)
        }
        return dynamic_style

    def config_enter_style(self, enter_bg_cite: str = "Theme.btn_enter_bg"):
        self.bind('<Enter>', lambda event: self.config(bg=eval(enter_bg_cite), cursor='hand2'))
        self.bind('<Leave>', lambda event: self.config(bg=eval(self.bg_cite)))


class ThemeLabel(Label):
    def __init__(self, parent, text, font, bg_cite: str = "Theme.win_bg", **kwargs):
        self.bg_cite = bg_cite
        super().__init__(parent, text=text, font=font, **self.get_dynamic_style, **kwargs, )

    @property
    def get_dynamic_style(self):
        dynamic_style = {
            "bg": eval(self.bg_cite),
            "foreground": Theme.main_fg
        }
        return dynamic_style


class ImageLabel(Label):
    overwrite = True

    def __init__(self, parent, default_img_id, **kwargs):
        self.default_imd_id = default_img_id
        self.image = ''
        super().__init__(parent, textvariable=self.default_imd_id, **kwargs)
        self.config(**self.get_dynamic_style)
        self.bind('<Button-3>', lambda event: self.create_menu.post(event.x_root, event.y_root))

    @property
    def get_dynamic_style(self):
        if not ImageLabel.overwrite:
            if not isinstance(self.cget("textvariable"), int):
                return {"bg": Theme.win_bg}
        abs_path = path.abspath(Theme.main_frame_img)
        img = Image.open(abs_path)
        photo = ImageTk.PhotoImage(img)
        self.image = photo
        return {
            "image": photo,
            "textvariable": self.default_imd_id,
            "bg": Theme.win_bg
        }

    @property
    def create_menu(self):
        img_path = self.cget("textvariable")
        i = 1 if isinstance(img_path, int) else 0
        states = ("active", "disabled")
        state = states[i]
        menu = Menu(self, tearoff=0, font=("宋体", 14))
        menu.add_command(label="打开图片", command=lambda: FileOperation.start_file(img_path),
                         state=state, image=open_ico, compound="left")
        menu.add_command(label="复制", command=lambda: FileOperation.copy_file(img_path),
                         state=state, image=copy_ico, compound="left")
        menu.add_command(label="复制路径", command=lambda: FileOperation.copy_file_path(img_path),
                         state=state, image=copy_path_ico, compound="left")
        menu.add_command(label="删除", command=lambda: self.remove_img(img_path),
                         state=state, image=delete_ico, compound="left")
        return menu

    def remove_img(self, img_path):
        if FileOperation.remove_file(img_path):
            self.config(**self.get_dynamic_style)


class ThemeEntry(Entry):
    frame_style = {
        "borderwidth": 1,
        "highlightthickness": 1,
        "relief": "flat"
    }

    def __init__(self, parent, start_pos=0, bg_cite="Theme.entry_bg",
                 highlightcolor="#007FD4", **kwargs):
        self.bg_cite = bg_cite
        self.start_pos = start_pos
        self.base_frame = Frame(parent, **ThemeEntry.frame_style, bg=eval(bg_cite))
        super().__init__(self.base_frame, relief="flat", **kwargs, )
        self.config(**self.get_dynamic_style)
        self.bind("<FocusIn>", self.base_frame.config(highlightcolor=highlightcolor))

    @property
    def get_dynamic_style(self):
        dynamic_style = {
            "bg": eval(self.bg_cite),
            "highlightbackground": Theme.win_bg,
            "foreground": Theme.main_fg,
            "insertbackground": Theme.main_fg
        }
        self.base_frame.config(bg=eval(self.bg_cite), highlightbackground=Theme.win_bg)
        return dynamic_style

    def place(self, x, y, width, height, **kwargs):
        self.base_frame.place(x=x, y=y, width=width, height=height)
        super().place(x=self.start_pos-1, y=-1, width=width-self.start_pos-2, height=height-2, **kwargs)


class ReadOnlyEntry(Entry):
    def __init__(self, parent, bg_cite="Theme.entry_bg", **kwargs):
        self.bg_cite = bg_cite
        super().__init__(parent, relief="flat", state="readonly", **kwargs)
        self.config(self.get_dynamic_style)
        self.bind("<Enter>", self.set_enter_mouse_state)

    @property
    def get_dynamic_style(self):
        dynamic_style = {
            "readonlybackground": eval(self.bg_cite),
            "foreground": Theme.main_fg,
        }
        return dynamic_style

    def refresh(self, content: str):
        self.config(state="normal")
        self.delete(0, "end")
        self.insert(0, content)
        self.config(state="readonly")

    def set_enter_mouse_state(self, _):
        content = self.get()
        if len(content) == 0:
            self.config(cursor="arrow")
        else:
            self.config(cursor="ibeam")


class ThemeListbox(Listbox):
    static_style = {
        "font": ('微软雅黑', 13),
        "relief": "flat",
        "borderwidth": -1
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **ThemeListbox.static_style,
                         **self.get_dynamic_style, **kwargs, )
        self.bind_scrollbar()

    def bind_scrollbar(self):
        scrollbar = Scrollbar(self, cursor="hand2")
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=self.yview)
        self.config(yscrollcommand=scrollbar.set)

    def load_folder(self, _, folder_path):
        self.delete(0, 'end')
        for file in scandir(folder_path):
            if re.match(r".*?\.(jpg|jpeg|png|spg)", file.name, re.I):
                self.insert('end', file.name)

    def open_file(self, _, folder_path):
        selected_indices = self.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        base_name = self.get(index)
        file_path = path.join(folder_path, base_name)
        if base_name.endswith("spg"):
            file_path = SpgManager.decompress_img(file_path)
        FileOperation.start_file(file_path)

    def adjust_task_list(self, _, pos):
        selected_indices = self.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        limit = 0 if pos == -1 else self.size() - 1
        if index == limit:
            return
        temp = self.get(index)
        self.delete(index)
        self.insert(index + pos, temp)
        self.select_set(index + pos)
        self.see(index + pos)

    def up_task_list(self, event):
        self.adjust_task_list(event, -1)

    def down_task_list(self, event):
        self.adjust_task_list(event, 1)

    def delete_current_select(self, _):
        selected_indices = self.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        self.delete(index)
        if index != self.size() - 1:
            self.select_set(index)
            self.see(index)

    def delete_all(self, _, ask_cancel=True):
        if ask_cancel:
            request = messagebox.askokcancel("提示", "您确定要清空\n整个任务列表吗?")
            if not request:
                return
        self.delete(0, 'end')

    @property
    def get_dynamic_style(self):
        dynamic_style = {
            "bg": Theme.win_bg,
            "foreground": Theme.main_fg,
            "highlightbackground": Theme.win_bg
        }
        return dynamic_style


class ThemeCanvas(Frame):
    draw_color = "#FF0000"
    style = {
        "bg": Theme.win_bg,
        "borderwidth": 0,
        "bd": 0,
        "relief": "flat",
        "highlightthickness": 0,
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **ThemeCanvas.style)
        self.photo = None
        self.__abs_canvas_width = 0
        self.__abs_canvas_height = 0
        self.__current_img_path = ""
        self.x_scrollbar = self.__set_x_scroll()
        self.extra_stuff_obj: tuple | None = None
        self.canvas = self.__set_canvas(highlightthickness=0, **kwargs)
        self.__undo_stack = []
        self.__redo_stack = []
        self.__draw_times = 0
        self.__rect_id = 0
        self.__start_x = 0
        self.__start_y = 0
        self.__offset = 0

    def place(self, x, y, width, height):
        super().place(x=x, y=y, width=width, height=height)
        self.canvas.place(x=-1, y=-1, width=width+4, height=height-12)
        self.extra_stuff(width, height)

    def extra_stuff(self, width, height):
        stuff_obj1 = Label(self, bg=Theme.scrollbar_bg)
        stuff_obj2 = Label(self, bg=Theme.scrollbar_bg)
        stuff_obj1.place(x=0, y=height - 13, width=1, height=13)
        stuff_obj2.place(x=width - 3, y=height - 13, width=3, height=13)
        self.extra_stuff_obj = stuff_obj1, stuff_obj2

    def __set_canvas(self, **kwargs):
        canvas = Canvas(self, bg=Theme.canvas_bg, **kwargs)
        canvas.configure(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.config(command=canvas.xview)
        window = Frame(canvas)
        canvas.create_window((0, 0), window=window, anchor='nw')
        self.photo, self.__abs_canvas_width, self.__abs_canvas_height = ImageApp.change_palette_img(
            canvas, path.abspath(Theme.crop_frame_img))
        return canvas

    @property
    def get_dynamic_style(self):
        if self.__current_img_path == "":
            self.photo, self.__abs_canvas_width, self.__abs_canvas_height = ImageApp.change_palette_img(
                self.canvas, path.abspath(Theme.crop_frame_img))
        self.canvas.config(bg=Theme.canvas_bg)
        for stuff in self.extra_stuff_obj:
            stuff.config(bg=Theme.scrollbar_bg)
        return {"bg": Theme.canvas_bg}

    def __set_x_scroll(self):
        x_scroll = Scrollbar(self, orient='horizontal', cursor="hand2")
        x_scroll.pack(side='bottom', fill='x')
        return x_scroll

    def bind_palette(self):
        self.canvas.bind('<Button-1>', self.__start_draw)
        self.canvas.bind('<B1-Motion>', self.__update_draw)
        self.canvas.bind('<ButtonRelease-1>', self.__end_draw)
        self.x_scrollbar.bind('<ButtonRelease-1>', self.__on_scroll)

    def unbind_palette(self):
        for event in self.canvas.bind():
            self.canvas.unbind(event)

    def __on_scroll(self, _):
        view_x1 = self.canvas.xview()[0]
        self.__offset = view_x1 * self.__abs_canvas_width

    def __start_draw(self, event):
        self.__start_x, self.__start_y = event.x + self.__offset, event.y
        if not (-1 < self.__start_x < self.__abs_canvas_width and -1 < self.__start_y < self.__abs_canvas_height):
            self.__rect_id = -1
            return
        self.__rect_id = (self.canvas. create_rectangle(
            self.__start_x, self.__start_y, self.__start_x, self.__start_y,
            outline=ThemeCanvas.draw_color, width=2))

    def __update_draw(self, event):
        # 更新矩形的大小
        if self.__rect_id == -1:
            return
        self.canvas.coords(self.__rect_id, self.__start_x,
                           self.__start_y, event.x + self.__offset, event.y)

    def __end_draw(self, event):
        # 更新矩形的大小
        if self.__rect_id == -1:
            return
        self.__undo_stack.append(self.__rect_id)
        x, y = self.__check_coords(event.x + self.__offset, event.y)
        self.canvas.coords(self.__rect_id, self.__start_x, self.__start_y, x, y)
        center_x, center_y = (self.__start_x + x) // 2, (self.__start_y + y) // 2
        self.__create_center_text(center_x, center_y)
        self.__redo_stack.clear()

    def __check_coords(self, x, y):
        x = max(2, min(x, self.__abs_canvas_width-1))
        y = max(2, min(y, self.__abs_canvas_height - 1))
        return x, y

    def change_img(self, img_path):
        def inner():
            self.photo, self.__abs_canvas_width, self.__abs_canvas_height = ImageApp.change_palette_img(
                self.canvas, img_path, judge_chinese=False)
        if self.__current_img_path == img_path:
            return
        self.__current_img_path = img_path
        self.canvas.delete("all")
        Thread(target=inner).start()
        self.__redo_stack.clear()
        self.__undo_stack.clear()
        self.__draw_times = 0

    def show_default_img(self):
        if self.__current_img_path == self.get_dynamic_style:
            return
        self.change_img(path.abspath(Theme.crop_frame_img))
        self.__current_img_path = ""
        self.unbind_palette()

    def __create_center_text(self, center_x, center_y):
        self.__draw_times += 1
        self.canvas.create_text(center_x, center_y, text=str(self.__draw_times),
                                font=('Arial', 18), fill=ThemeCanvas.draw_color)

    def undo(self, _):
        if len(self.__undo_stack) == 0:
            return
        self.__draw_times -= 1
        delete_id = self.__undo_stack.pop()
        coords = self.canvas.coords(delete_id)
        self.__redo_stack.append(coords)
        self.canvas.delete(delete_id, delete_id + 1)

    def redo(self, _):
        if len(self.__redo_stack) == 0:
            return
        x1, y1, x2, y2 = self.__redo_stack.pop()
        self.__rect_id = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                      outline=ThemeCanvas.draw_color, width=2)
        self.__create_center_text((x1 + x2) // 2, (y1 + y2) // 2)
        self.__undo_stack.append(self.__rect_id)

    def is_edit(self) -> bool:
        return self.__draw_times != 0

    @property
    def get_current_img_path(self):
        return self.__current_img_path

    @property
    def get_all_draw_coords(self) -> list:
        return [self.canvas.coords(draw_id) for draw_id in self.__undo_stack]


class ToningCanvas(Canvas):
    def __init__(self, parent, colours: list, **kwargs):
        self.colors = colours
        self.__before_max_draw_id = -1
        self.__max_draw_id = -1
        super().__init__(parent, self.get_dynamic_style, highlightthickness=0, **kwargs)
        self.__create_toning_circle()

    @property
    def get_dynamic_style(self):
        style = {
            "bg": Theme.win_bg,
        }
        return style

    def __create_highlight_circle(self, pos: int):
        self.__max_draw_id = self.create_oval(pos - 4, 6, pos + 22, 32, outline="#A6A6A6")

    def __vanish_highlight_circle(self, _):
        if self.__max_draw_id == -1:
            return
        self.delete(self.__max_draw_id)

    def __choose_color(self, colour):
        if self.__before_max_draw_id != -1:
            self.delete(self.__before_max_draw_id)
        self.__before_max_draw_id = self.__max_draw_id
        ThemeCanvas.draw_color = colour
        self.itemconfig(self.__max_draw_id, outline="#000000")
        self.__max_draw_id = -1

    def __create_toning_circle(self):
        for i, color in enumerate(self.colors):
            x = 10 + i * 28
            self.create_oval(x, 10, x + 18, 28, fill=color, tags=color, width=0.1)
            self.tag_bind(color, "<Enter>", lambda event, pos=x: self.__create_highlight_circle(pos))
            self.tag_bind(color, "<Leave>", self.__vanish_highlight_circle)
            self.tag_bind(color, "<Button-1>", lambda event, colour=color: self.__choose_color(colour))


class FileTreeView(Treeview):
    rowheight = 23
    font = tk_font.Font(family="微软雅黑", size=12)
    global_style.configure("Treeview", rowheight=rowheight, font=font, relief="flat")

    def __init__(self, parent, width, height, **kwargs):
        self.concealed_label = None
        self.parent = parent
        self.place_info = (width, height)
        self.__open_nodes = []
        self.outer_link = lambda: None
        super().__init__(self.parent, show="tree", **kwargs, **self.get_dynamic_style)
        self.__bind_events()

    @property
    def get_dynamic_style(self):
        if self.concealed_label:
            self.concealed_label.config(bg=Theme.win_bg)
        global_style.configure(
            "Treeview",
            background=Theme.win_bg,
            foreground=Theme.main_fg,
            fieldbackground=Theme.win_bg,
            lightcolor=Theme.win_bg,
            bordercolor=Theme.win_bg
        )
        return {}

    def __bind_events(self):
        width, height = self.place_info
        v_scrollbar = Scrollbar(self, orient="vertical", command=self.yview, cursor="hand2")
        v_scrollbar.place(x=width-13, y=-13, height=height+16)
        h_scrollbar = Scrollbar(self, orient="horizontal", command=self.xview, cursor="hand2")
        h_scrollbar.place(x=-13, y=height-13, width=width+16)
        self.concealed_label = Label(self, bg=Theme.win_bg)
        self.concealed_label.place(x=width-12, y=height-13, width=12, height=13)
        self.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.column("#0", minwidth=1200, width=1200)
        # bind event
        self.bind("<<TreeviewOpen>>", self.lazy_load_file)
        self.bind("<<TreeviewClose>>", self.clear_memory)
        self.bind("<Double-Button-1>", self.open_file)
        self.bind('<Button-3>', self.create_menu)

    def open_file(self, event):
        item = self.identify_row(event.y)
        if len(item) == 0:
            return
        file_path = self.get_selected_abs_path(item)
        if path.isdir(file_path):
            return
        FileOperation.start_file(file_path)

    def create_menu(self, event):
        # 让右键点击也能选中行
        item = self.identify_row(event.y)
        if len(item) == 0:
            return
        self.selection_set(item)
        selected_file_path = self.get_selected_abs_path(item)
        menu = Menu(self, tearoff=0, font=("宋体", 14))
        menu.add_command(label="打开文件", command=lambda: FileOperation.start_file(selected_file_path),
                         image=open_ico, compound='left')
        menu.add_command(label="复制文件", command=lambda: FileOperation.copy_file(selected_file_path),
                         image=copy_ico, compound='left')
        menu.add_command(label="复制路径", command=lambda: FileOperation.copy_file_path(selected_file_path),
                         image=copy_path_ico, compound='left')
        menu.add_command(label="删除文件", command=lambda: self.outer_link(),
                         image=delete_ico, compound='left')
        menu.post(event.x_root, event.y_root)

    def build_catalog_tree(self, base_folder, root=None):
        if not root:
            self.delete(*self.get_children())
            root = self.insert("", 0, text=base_folder, open=True, image=folder_img)
            self.__open_nodes.clear()
            self.__open_nodes.append(root)
        for file in scandir(base_folder):
            if not re.match(r".*?\.(jpg|png|jpeg)", file.name, re.I) and path.isfile(file.path):
                continue
            if path.isfile(file.path):
                self.insert(root, 0, text=file.name, image=img_file)
            else:
                dir_node = self.insert(root, 0, text=file.name, image=folder_img)
                self.insert(dir_node, 0) if FileJudgement.contains_img_or_folder(file.path) else 0

    def get_selected_abs_path(self, item):
        parent_id = super().parent(item)
        base_name = self.item(item)["text"]
        dir_name = self.item(parent_id)["text"]
        while dir_name != "":
            base_name = path.join(dir_name, base_name)
            parent_id = super().parent(parent_id)
            dir_name = self.item(parent_id)["text"]
        return base_name

    def lazy_load_file(self, _):
        item = self.selection()[0]
        self.delete(*self.get_children(item))
        base_name = self.get_selected_abs_path(item)
        self.build_catalog_tree(base_name, item)
        self.__open_nodes.append(item)

    def clear_memory(self, _):
        item = self.selection()[0]
        self.delete(*self.get_children(item))
        self.insert(item, 0)
        self.__open_nodes.remove(item)

    def search_node(self, key: str):
        results = []
        for open_node in self.__open_nodes:
            try:
                for child in self.get_children(open_node):
                    # Error proved that the original node is destroyed.
                    results.append(child) if re.search(key, self.item(child, "text")) else 0
            except TclError:
                continue

        return results

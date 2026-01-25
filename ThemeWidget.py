from Config import Theme
from tkinter import Label, Listbox, Canvas, Frame, messagebox
from tkinter_extension.Widget.Command import FileCommand
from ImageApp import Image, ImageTk, ImageApp
from FileManager import SpgManager
from os import path, scandir
from threading import Thread
import re


class ImageLabel(Label):
    overwrite = True

    def __init__(self, parent, default_img_id, **kwargs):
        self.default_imd_id = default_img_id
        self.image = ''
        super().__init__(parent, textvariable=self.default_imd_id, **kwargs)
        self.config(**self.get_dynamic_style)

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

    def remove_img(self, img_path):
        if FileCommand.FileOperation.remove_file(img_path):
            self.config(**self.get_dynamic_style)


class TaskListbox(Listbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, )

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
        FileCommand.FileOperation.start_file(file_path)

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


class ThemeCanvas(Frame):
    draw_color = "#FF0000"
    style = {
        "bg": Theme.win_bg,
        "borderwidth": 0,
        "bd": 0,
        "relief": "flat",
        "highlightthickness": 0,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, **ThemeCanvas.style)
        self.photo = None
        self.__abs_canvas_width = 0
        self.__abs_canvas_height = 0
        self.__current_img_path = ""
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

    def __set_canvas(self, **kwargs):
        canvas = Canvas(self, bg=Theme.canvas_bg, **kwargs)
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
        return {"bg": Theme.canvas_bg}

    def bind_palette(self):
        self.canvas.bind('<Button-1>', self.__start_draw)
        self.canvas.bind('<B1-Motion>', self.__update_draw)
        self.canvas.bind('<ButtonRelease-1>', self.__end_draw)

    def unbind_palette(self):
        for event in self.canvas.bind():
            self.canvas.unbind(event)

    def on_scroll(self, _):
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
        self.canvas.coords(
            self.__rect_id,
            self.__start_x,
            self.__start_y,
            event.x + self.__offset, event.y
        )

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

    def __create_center_text(self, center_x, center_y) -> None:
        self.__draw_times += 1
        self.canvas.create_text(
            center_x, center_y,
            text=str(self.__draw_times),
            font=('Arial', 18),
            fill=ThemeCanvas.draw_color
        )

    def undo(self, _) -> None:
        if len(self.__undo_stack) == 0:
            return
        self.__draw_times -= 1
        delete_id = self.__undo_stack.pop()
        coords = self.canvas.coords(delete_id)
        self.__redo_stack.append(coords)
        self.canvas.delete(delete_id, delete_id + 1)

    def redo(self, _) -> None:
        if len(self.__redo_stack) == 0:
            return
        x1, y1, x2, y2 = self.__redo_stack.pop()
        self.__rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline=ThemeCanvas.draw_color, width=2
        )
        self.__create_center_text((x1 + x2) // 2, (y1 + y2) // 2)
        self.__undo_stack.append(self.__rect_id)

    def is_edit(self) -> bool:
        return self.__draw_times != 0

    @property
    def get_current_img_path(self) -> str:
        return self.__current_img_path

    @property
    def get_all_draw_coords(self) -> list:
        return [self.canvas.coords(draw_id) for draw_id in self.__undo_stack]

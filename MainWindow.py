from tkinter import Frame, Tk, Button, Menu
from Config import Theme


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.current_theme = Theme.load_default_theme()
        self.__win()
        (menu_bar, self.file_menu, self.theme_menu, self.help_menu) = self.__set_menu()
        self.config(menu=menu_bar)
        # 三大模式
        self.main_frame: Frame = self.set_main_frame()
        self.crop_frame: Frame = Frame()
        self.current_mode: int = 0
        self.switch_frame = self.__set_switch_frame()
        self.main_mode_btn = self.__set_main_mode_btn(self.switch_frame)
        self.crop_mode_btn = self.__set_crop_mode_btn(self.switch_frame)
        self.set_widget_color()

    def __win(self):
        self.resizable(False, False)
        self.configure(background=Theme.win_bg, )
        self.title("GFPGAN")
        width, height = 950, 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

    def set_main_frame(self):
        main_frame = Frame(self)
        main_frame.place(x=50, y=0, width=900, height=500)
        return main_frame

    def __set_switch_frame(self):
        frame = Frame(self)
        frame.place(x=0, y=0, width=50, height=500)
        return frame

    @staticmethod
    def __set_main_mode_btn(parent):
        # 默认选择主模式
        btn = Button(parent, text="人\n脸\n超\n分\n辨\n率", relief='flat', font=('宋体', 22))
        btn.place(x=0, y=0, height=243, width=50)
        return btn

    @staticmethod
    def __set_crop_mode_btn(parent):
        btn = Button(parent, text="裁\n剪\n人\n脸", relief='flat', font=('宋体', 22))
        btn.place(x=0, y=243, height=257, width=50)
        return btn

    def __set_menu(self):
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        theme_menu = Menu(menu_bar, tearoff=0)
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        menu_bar.add_cascade(label="主题", menu=theme_menu)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        return menu_bar, file_menu, theme_menu, help_menu

    def set_widget_color(self):
        self.main_frame.config(bg=Theme.win_bg)
        self.crop_frame.config(bg=Theme.win_bg)
        self.main_mode_btn.config(**Theme.style_dict["FrameButton"], bg=Theme.switch_frame_bg)
        self.crop_mode_btn.config(Theme.style_dict["FrameButton"], bg=Theme.switch_frame_unselect_bg)

from Config import Theme
from threading import Thread
from MainWindow import MainWindow
from tkinter import messagebox, Label, Toplevel
from os import path, startfile


class Control(MainWindow):
    def __init__(self):
        super().__init__()
        self.crop_mode = None
        from MainFrameControl import GuiControl
        self.main_mode = GuiControl(self.main_frame)
        Thread(target=self.__bind).start()
        Thread(target=self.initialize_crop_frame).start()

    def __bind(self):
        self.iconbitmap("Data/favicon.ico")
        self.protocol('WM_DELETE_WINDOW', self.destroy_window)
        self.main_mode_btn.config(command=self.switch_to_main_mode)
        self.crop_mode_btn.config(command=self.switch_to_crop_mode)
        self.file_menu.add_command(label="导入单张图片", command=self.load_single_img)
        self.file_menu.add_command(label="导入spg文件", command=self.load_spg_file)
        self.file_menu.add_command(label="保存当前配置", command=self.main_mode.save_current_setting)
        self.file_menu.add_command(label="清空当前数据", command=self.main_mode.clear_all)
        self.help_menu.add_command(label="版权声明", command=self.__show_copyright)
        self.help_menu.add_command(label="使用说明", command=self.__show_how_to_use)
        self.help_menu.add_command(label="错误日志", command=self.__show_error_log)
        for theme in Theme.search_available_theme():
            self.add_theme_command(theme)

    def add_theme_command(self, theme):
        self.theme_menu.add_command(label=theme, command=lambda: self.switch_theme(theme))

    def destroy_window(self):
        from SharedDatabase import SharedVariable, SendData
        SharedVariable.kill_subprocess()
        SendData.clear_all_table()
        self.destroy()

    def __show_copyright(self):
        copyright_win = self.__show_sub_window("版权声明", 300, 80)
        copyright_win.iconbitmap('Data/favicon.ico')
        Label(copyright_win, text="原项目地址:\n https://github.com/TencentARC/GFPGAN\n"
              "严禁使用者二次售卖该程序，允许无偿传播。\n如有侵权请联系作者删除, 邮箱:1504891917@qq.com").pack()

    def __show_sub_window(self, title, width, height):
        sub_window = Toplevel(self)
        sub_window.title(title)
        sub_window.resizable(False, False)
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        sub_window.geometry(geometry)
        return sub_window

    @staticmethod
    def __show_how_to_use():
        file = open("Data/readme.txt", "w", encoding="utf-8")
        file.write("""①主界面右下角的任务列表会显示待处理的模糊图片，如果没有图片，
点击开始处理后,程序仍然会花费时间去加载模型，直到检测没有需要
处理图片时会自动显示处理完成。因此在点击开始处理前请先确定右下角的
任务列表有任务可以处理。\n
②重点提示: 在选择文件夹时，不允许选择路径包含中文的文件夹, 待处理的图片
也不允许包含中文，程序会自动跳过中文名图片不予处理。\n
③处理图片的参数只保留了一个图片缩放比例，缩放越大，图片处理后清晰度越高，
但将导致图片体积增大，图片失真概率增加，需权衡调整。\n
④裁剪人脸部分可以通过手动裁剪图片的局部, 做到只处理图片模糊的局部，能够
显著提高图片处理速度。截取图片会被导出为SPG归档文件, 可以直接放入输入文件夹
让程序处理。\n
⑤图片处理后分四个文件夹存放，其中: 
(1)restored_images保存了最终处理好的图片。
(2)cmp保存了处理前后人脸图片的对比图,。
(3)cropped_faces保存了从原图中裁剪出来的人脸图片;
(4)restored_faces保存了程序清晰化处理后的人脸图片;
""")
        file.close()
        startfile(path.abspath("Data/readme.txt"))

    @staticmethod
    def __show_error_log():
        error_log_path = path.abspath("Data/Error_log.txt")
        if not path.isfile(error_log_path):
            with open(error_log_path, 'w'):
                pass
        startfile(error_log_path)

    def switch_to_main_mode(self):
        if not self.current_mode:
            return
        self.crop_frame.place_forget()
        self.main_mode_btn.config(bg=Theme.switch_frame_bg)
        self.crop_mode_btn.config(bg=Theme.switch_frame_unselect_bg)
        self.main_frame.place(x=50, y=0, width=900, height=500)
        self.current_mode = 0

    def switch_to_crop_mode(self):
        if self.current_mode:
            return
        self.main_frame.place_forget()
        self.crop_mode_btn.config(bg=Theme.switch_frame_bg)
        self.main_mode_btn.config(bg=Theme.switch_frame_unselect_bg)
        self.crop_frame.place(x=50, y=0, width=900, height=500)
        self.current_mode = 1

    def initialize_crop_frame(self):
        from CropFrameControl import CropControl
        self.crop_mode = CropControl(self.crop_frame)

    def switch_theme(self, theme):
        if theme == self.current_theme:
            return
        self.current_theme = theme
        Theme.load_theme(theme)
        self.set_widget_color()
        working = True if self.main_mode.execute_btn.cget("bg") == "salmon" else False
        self.main_mode.update_widget_color()
        self.crop_mode.update_widget_color()
        if working:
            bg = self.main_mode.execute_btn.cget("bg")
            self.main_mode.execute_btn.config(bg=bg)

    def load_single_img(self):
        if self.current_mode == 0:
            self.main_mode.load_single_picture()
        else:
            self.crop_mode.open_img_file(0)

    def load_spg_file(self):
        if self.current_mode == 0:
            self.main_mode.load_spg_file()
        else:
            messagebox.showinfo("提示", "裁剪模式下不支持查看SPG文件!")

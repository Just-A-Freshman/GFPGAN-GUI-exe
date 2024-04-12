import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar, ttk
from subprocess import Popen, PIPE, STDOUT
from PIL import Image, ImageTk, UnidentifiedImageError
from os import path, scandir, makedirs, system, getcwd, listdir
from re import match, search
from threading import Thread


class GUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.img_app = ImageApp()
        self.infile_path = None
        self.outfile_path = None
        self.infile_path_entry = None
        self.output_folder_entry = None
        self.img_label1 = None
        self.img_label2 = None
        self.open_button1 = None
        self.open_button2 = None
        self.original_frame = None
        self.dealt_frame = None
        self.command_frame = None
        self.output_info_frame = None
        self.extension_combobox = None
        self.img_up_sampler_slider = None
        self.img_up_sampler = tk.IntVar(value=2)
        self.bg_up_sampler = tk.IntVar(value=400)
        self.output_text = None
        self.set_all_element()

    def set_all_element(self):
        # 布置所有控件
        self.set_root_win()
        self.set_frame()
        self.set_info_label()
        self.set_open_button()
        self.set_entry_and_output_text()
        self.show_default_img()
        self.set_combobox()
        self.set_slider()
        self.root.mainloop()

    def set_root_win(self):
        self.root.resizable(False, False)
        self.root.title("超分辨率处理GUI")
        self.root.geometry('1080x650+300+100')

    def set_frame(self):
        self.original_frame = tk.Frame(self.root, borderwidth=2, relief='solid',
                                       highlightbackground='gray', highlightthickness=3)
        self.dealt_frame = tk.Frame(self.root, borderwidth=2, relief='solid',
                                    highlightbackground='gray', highlightthickness=3)
        self.command_frame = tk.Frame(self.root, borderwidth=2, relief='solid')
        self.output_info_frame = tk.Frame(self.root, borderwidth=2, relief='solid')
        self.command_frame.place(x=0, y=322, height=328, width=540)
        self.output_info_frame.place(x=540, y=322, height=328, width=540)

    def set_info_label(self):
        label1 = tk.Label(self.root, text='原图', font=('宋体', 17))
        label2 = tk.Label(self.root, text='处理后图片', font=('宋体', 17))
        label3 = tk.Label(self.root, text='图片输入路径:', font=('宋体', 16))
        label4 = tk.Label(self.root, text='图片输出路径:', font=('宋体', 16))
        label5 = tk.Label(self.root, text='脸部上采样度:', font=('宋体', 16))
        label6 = tk.Label(self.root, text='背景采样尺寸:', font=('宋体', 16))
        label7 = tk.Label(self.root, text='输出文件格式:', font=('宋体', 16))
        label1.place(x=210, y=293)
        label2.place(x=780, y=293)
        label3.place(x=25, y=340)
        label4.place(x=25, y=390)
        label5.place(x=25, y=490)
        label6.place(x=25, y=540)
        label7.place(x=25, y=440)

    def set_open_button(self):
        self.open_button1 = tk.Button(self.root, text="预览图片", bg="wheat", font=('宋体', 13),
                                      command=lambda: messagebox.showinfo('提示', '当前没有图片可预览!'))
        self.open_button2 = tk.Button(self.root, text="预览图片", bg="wheat", font=('宋体', 13),
                                      command=lambda: messagebox.showinfo('提示', '当前没有图片可预览!'))
        open_folder1 = tk.Button(self.root, text="打开文件夹", bg="wheat", font=('宋体', 13),
                                 command=lambda: self.img_app.open_folder(self.infile_path))
        open_folder2 = tk.Button(self.root, text="打开文件夹", bg="wheat", font=('宋体', 13),
                                 command=lambda: self.img_app.open_folder(self.outfile_path))
        choose_folder1 = tk.Button(self.root, text='选择文件夹', bg="wheat",
                                   command=lambda: self.choose_folder(1))
        choose_folder2 = tk.Button(self.root, text='选择文件夹', bg='wheat',
                                   command=lambda: self.choose_folder(2))
        execute_btn = tk.Button(self.root, text='开始图片处理', font=('宋体', 16),
                                bg='peachpuff', command=self.execute_entry)
        self.open_button1.place(x=290, y=293, width=80)
        self.open_button2.place(x=570, y=293)
        open_folder1.place(x=378, y=293)
        open_folder2.place(x=660, y=293)
        choose_folder1.place(x=378, y=340, width=75)
        choose_folder2.place(x=378, y=390, height=30)
        execute_btn.place(x=200, y=590)

    def set_entry_and_output_text(self):
        self.infile_path_entry = tk.Entry(self.root, width=30)
        self.infile_path_entry.place(x=165, y=340, height=30)
        self.output_folder_entry = tk.Entry(self.root, width=30)
        self.output_folder_entry.place(x=165, y=390, height=30)
        output_scrollbar = Scrollbar(self.root)
        output_scrollbar.place(x=1060, y=325, height=320)
        self.output_text = tk.Text(self.root, font=('宋体', 18))
        self.output_text.place(x=542, y=323, width=518, height=323)  # width=535
        self.output_text.config(yscrollcommand=output_scrollbar.set)
        output_scrollbar.config(command=self.output_text.yview)

    def set_combobox(self):
        self.extension_combobox = ttk.Combobox(self.root, values=['auto', 'png', 'jpg', 'jpeg'])
        self.extension_combobox.insert(tk.END, 'auto')
        self.extension_combobox.config(state='readonly')
        self.extension_combobox.place(x=165, y=440, width=80, height=30)

    def set_slider(self):
        img_up_sampler_slider = tk.Scale(self.root, from_=1, to=8, orient=tk.HORIZONTAL,
                                         variable=self.img_up_sampler, width=25)
        bg_up_sampler_slider = tk.Scale(self.root, from_=0, to=2000, orient=tk.HORIZONTAL,
                                        variable=self.bg_up_sampler, width=25)
        img_up_sampler_slider.place(x=165, y=470, width=80)
        bg_up_sampler_slider.place(x=165, y=520, width=220)

    def choose_folder(self, flag):
        if flag == 1:
            folder_selected = filedialog.askdirectory(initialdir=self.infile_path)
            if not folder_selected:
                return
            self.infile_path_entry.delete(0, 'end')
            self.infile_path_entry.insert(0, folder_selected)
            self.infile_path = folder_selected
        else:
            folder_selected = filedialog.askdirectory(initialdir=self.outfile_path)
            if not folder_selected:
                return
            self.output_folder_entry.delete(0, 'end')
            self.output_folder_entry.insert(0, folder_selected)
            self.outfile_path = folder_selected

    def show_default_img(self):
        original_img = Image.open("Load_picture/Default.jpg").copy()
        dealt_img = Image.open("Load_picture/Default.jpg").copy()
        original_img.thumbnail((540, 292), Image.LANCZOS)
        dealt_img.thumbnail((540, 292), Image.LANCZOS)
        photo1 = ImageTk.PhotoImage(original_img)
        photo2 = ImageTk.PhotoImage(dealt_img)
        self.img_label1 = tk.Label(self.original_frame, image=photo1)
        self.img_label2 = tk.Label(self.dealt_frame, image=photo2)
        self.img_label1.pack(fill=tk.BOTH, expand=True)
        self.img_label2.pack(fill=tk.BOTH, expand=True)
        self.img_label1.image = photo1
        self.img_label2.image = photo2
        self.original_frame.place(x=0, y=0, height=291.6, width=540)
        self.dealt_frame.place(x=540, y=0, height=291.6, width=540)

    def first_check(self):
        infile_path = self.infile_path_entry.get()
        outfile_path = self.output_folder_entry.get()
        if infile_path == '' or outfile_path == '':
            messagebox.showinfo('提示', '文件输入或输出\n路径不能为空!')
            return True
        elif not path.exists(infile_path):
            messagebox.showerror('错误', '文件输入路径不存在!')
            return True
        elif path.isfile(infile_path) or path.isfile(outfile_path):
            messagebox.showerror('错误', '\n输入与输出路径都只允许为文件夹!')
            return True
        elif search(r'[\u4e00-\u9fff]', f'{infile_path}{outfile_path}'):
            messagebox.showerror('错误', '文件路径不允许包含中文,\n否则将导致程序异常终止!')
            return True
        else:
            return False

    def execute_entry(self):
        # 传入基本参数
        if self.first_check():
            return
        self.img_app.folder_path = self.outfile_path
        with open('load_data.txt', 'w', encoding='utf-8') as f:
            f.write(f'{self.infile_path}\n{self.outfile_path}\n{self.img_up_sampler.get()}\n')
            f.write(f'{self.bg_up_sampler.get()}\n\n0\n{self.extension_combobox.get()}\n0.5')
        # 传入大量必要参数
        exe = ExecuteCommand(self.infile_path, self.outfile_path, self.output_text,
                             self.img_app, self.img_label1, self.img_label2, self.open_button1, self.open_button2)
        exe.main_entry()


class ImageApp(object):
    @staticmethod
    def open_folder(folder_path):
        if folder_path is None:
            messagebox.showinfo('提示', '当前未选择文件路径!')
            return
        # 这一步替换异常关键，我发现用'/'没法跳转到正确路径,估计和系统有关
        folder_path = folder_path.replace('/', '\\')
        Popen(['explorer', folder_path], shell=True)

    @staticmethod
    def open_img(img_path):
        if img_path is None:
            img_path = "Load_picture/Default.jpg"
        Popen(['start', img_path], shell=True)

    @staticmethod
    def resize_image(image_path):
        # 先给权限!
        Image.MAX_IMAGE_PIXELS = 314572800
        with Image.open(image_path) as img:
            w, h = img.size
            new_img = img.resize((w // 2, h // 2), Image.LANCZOS)
            new_img.save(image_path)

    @staticmethod
    def change_img(img_label: tk.Label, img_path):
        with Image.open(img_path).copy() as img:
            img.thumbnail((540, 292), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo)
            # 保持对新图片的引用
            img_label.image = photo


class ExecuteCommand:
    def __init__(self, infile_path, outfile_path, output_text, img_app,
                 input_label, output_label, open_btn1, open_btn2):
        self.current_work = getcwd()
        self.NotFileToDeal = False
        self.temp_folder = path.join(self.current_work, 'temp')
        self.error_list = []
        self.infile_path = infile_path
        self.outfile_path = outfile_path
        self.output_text = output_text
        self.img_app = img_app
        self.input_label = input_label
        self.output_label = output_label
        self.open_btn1 = open_btn1
        self.open_btn2 = open_btn2

    def main_entry(self):
        check_thread = Thread(target=self.check_infile_path)
        check_thread.start()
        Thread(target=self.execute_in_cmd, args=(check_thread, )).start()

    def check_if_folder(self, infile_path):
        if path.isdir(infile_path):
            system(f'move "{infile_path}" temp')
            self.error_list.append(path.basename(infile_path))
            self.output_text.insert(f'\n警告: {infile_path}是文件夹，\n可能导致程序最终运行报错'
                                    f'\n已经被临时移动到[{self.temp_folder}]下!\n')
            self.output_text.see(tk.END)

    def check_if_contains_chinese(self, infile_path):
        img_name = path.basename(infile_path)
        if search(r'[\u4e00-\u9fff]', img_name):
            system(f'move "{infile_path}" temp')
            self.error_list.append(path.basename(img_name))
            self.output_text.insert(tk.END, f'\n警告: 图片路径[{img_name}]包含中文,\n将导致最终图片保存错误!'
                                    f'\n为避免程序运行最终出错,\n已经被临时移动到[{self.temp_folder}]下!\n')
            self.output_text.see(tk.END)

    def prevent_decompression_bomb(self, infile_path) -> bool:
        """
        infile_path should be a PathLikeStr and a file path.
        """
        try:
            Image.MAX_IMAGE_PIXELS = 31457280
            # 用上下文管理器，否则报错Image就不会自己关闭了!
            with Image.open(infile_path):
                pass
            return False

        except Image.DecompressionBombWarning as e:
            image_decompress_size = int(search(r'Image size \((\d+?) pixels\)', str(e)).group(1))
            self.output_text.insert(tk.END, f'\n图片:[{infile_path}]解压缩后体积为'
                                            f'[{image_decompress_size / 1024 / 1024:.2f}MB]'
                                            f'超过30MB, 无法继续处理!\n')
            return True

        except UnidentifiedImageError:
            system(f'move "{infile_path}" temp')
            self.error_list.append(path.basename(infile_path))
            self.output_text.insert(tk.END, f'\n无法识别图片文件:\n[{path.basename(infile_path)}]\n'
                                            f'为不影响后续处理,已被临时移入目录:\n[{self.temp_folder}]\n')
            self.output_text.see(tk.END)
            return True
        finally:
            Image.MAX_IMAGE_PIXELS = 89478485

    def check_infile_path(self):
        # 务必检查清楚输入路径有没有什么不干净的东西!
        self.output_text.insert(tk.END, '正在检查输入路径......\n')
        files = scandir(self.infile_path)
        # If temp folder is deliberate removal, it will raise NotSuchFileError,
        # So we must make it exist.
        makedirs('temp', exist_ok=True)
        for file in files:
            self.check_if_folder(file.path)
            self.prevent_decompression_bomb(file.path)
            self.check_if_contains_chinese(file.path)

        if len(listdir(self.infile_path)) == 0:
            self.output_text.insert(tk.END, f'\n文件夹[{self.infile_path}]中没有文件可处理!\n')
            self.restore_img()
            self.NotFileToDeal = True

    def load_prev_processed_img(self, input_file_path):
        """
        input_file_path refer to the input image of the finish processed image.
        It can be None. If it's not None, it should be a match Object.
        """
        if input_file_path:
            input_filename = input_file_path.group(1)
            input_file_path = path.join(self.infile_path, input_filename)
            self.open_btn1.config(command=lambda: self.img_app.open_img(input_file_path))
            self.img_app.change_img(self.input_label, input_file_path)

    def twice_deal_outfile_img(self, output_file_path):
        try:
            if path.getsize(output_file_path) > 10485760:
                self.img_app.resize_img(output_file_path)
            self.open_btn2.config(command=lambda: self.img_app.open_img(output_file_path))
            self.img_app.change_img(self.output_label, output_file_path)

        except Image.DecompressionBombError:
            self.output_text.insert(tk.END, f'\n生成图片:\n[{output_file_path}]\n过大，无法压缩!\n')

        except OSError:
            self.output_text.insert(tk.END, f'\n输出图片似乎被移出了文件夹,\n无法加载到预览面板上!\n')
        finally:
            # In Class-ImageApp function-resize_img, it's turned up to 200MB to make it possible to
            # shrink the big image, but after the resize we must restore the value.
            Image.MAX_IMAGE_PIXELS = 89478485

    def execute_in_cmd(self, check_thread: Thread):
        check_thread.join()
        if self.NotFileToDeal:
            return
        messagebox.showinfo('提示', '开始处理!')
        self.output_text.insert(tk.END, f'\n模型程序启动中......\n')
        process = Popen('GFPGAN.py', stdout=PIPE, stderr=STDOUT,
                        shell=True, text=True, encoding='utf-8')

        infile_img = None
        try:
            for line in iter(process.stdout.readline, ''):
                if search('[Ww]arning', line):
                    continue
                temp = match(r'正在处理图片\[(.*?)]......', line)
                infile_img = temp if temp else infile_img
                finsh_processed_img = match(r'图片处理完成，已保存在\[(.*?)]路径下!', line)
                self.output_text.insert(tk.END, line)
                self.output_text.see(tk.END)
                if finsh_processed_img:
                    output_file_path = finsh_processed_img.group(1)
                    self.load_prev_processed_img(infile_img)
                    self.twice_deal_outfile_img(output_file_path)
        except UnicodeDecodeError as e:
            self.output_text.insert(tk.END, f'出现异常:\n{e}\n中断了后续提示信息的输出!\n')

        self.restore_img()
        messagebox.showinfo('提示', '处理完成!')

    def restore_img(self):
        for file in self.error_list:
            try:
                system(fr'move "temp\{file}" "{self.infile_path}"')
                self.output_text.insert(tk.END, f'\n已将未处理文件[{file}]\n移回目录[{self.infile_path}]中!\n')
            except Exception as e:
                self.output_text.insert(tk.END, f'\n在将文件[{path.join(self.current_work, file)}]\n'
                                                f'移动回原目录[{self.infile_path}]时出现错误, 错误原因:\n{e}\n')
        self.error_list.clear()


if __name__ == '__main__':
    Gui = GUI()

from threading import Thread
from tkinter import messagebox
from SharedDatabase import SharedVariable
from Config import Theme
from re import match
from os import path
import subprocess


class ExecuteCommand:
    def __init__(self, page_manager, main_frame_control):
        # Two class
        self.page_manager = page_manager
        self.main_frame_control = main_frame_control
        # command:
        self.__stop = False
        self.__current_img = ""
        self.__is_spg = False
        self.__progress = 0
        self.__total = 0
        self.__step = 3

    @staticmethod
    def decode_output_text(line):
        decode_list = ('utf-8', 'gbk', 'ascii', 'gb2312', 'utf-16', 'cp1252')
        for code in decode_list:
            try:
                line = line.decode(code)
                return line if '' not in line else ""
            except UnicodeDecodeError:
                continue
        return ""

    def set_stop_signal(self):
        self.main_frame_control.execute_btn.config(bg="#E08C79", state="disabled", text="终止程序中...")
        self.__stop = True

    def __update_progress(self, line):
        match_result = match(r"\?<(.*)>", line)
        if not match_result:
            return
        match_result = match_result.group(1)
        prefix = match_result[:5]
        suffix = match_result[6:]
        match prefix:
            case "doing": self.update_tip()
            case "start": self.initialize_show_widget(suffix)
            case "total": self.get_total_progress(suffix)
            case "#done": self.tidy_up(suffix)
            case "#bad": self.main_frame_control.overwrite_to_show_label(f"无法识别spg文件:{suffix}")

    def get_total_progress(self, suffix):
        if self.__is_spg:
            self.__total = int(suffix) * 10 + 5
            self.__step = round(91 / self.__total, 3)
        else:
            self.__total = int(suffix) * 2 + 10
            self.__step = round(76 / (self.__total - 8), 3)

    def update_tip(self):
        self.__progress += 1
        self.main_frame_control.overwrite_to_show_label(
            f"正在处理: {self.__current_img}"
            f"({self.__progress} / {self.__total})...")
        self.main_frame_control.progressbar.step(self.__step)

    def tidy_up(self, img_path):
        if img_path == "":
            self.main_frame_control.send_task()
            return
        self.main_frame_control.overwrite_to_show_label(f"图片{path.basename(img_path)}已处理完成!")
        self.page_manager.finish_signal = True
        self.main_frame_control.progressbar.set(100)
        self.main_frame_control.send_task()
        self.__step = 3

    def initialize_show_widget(self, img_path):
        self.main_frame_control.progressbar.set(0)
        base_name = path.basename(img_path)
        self.main_frame_control.overwrite_to_show_label(f"正在处理: {base_name}...")
        self.__current_img = base_name
        self.__progress = 0
        if base_name.endswith("spg"):
            self.__is_spg = True
        else:
            self.__is_spg = False
            self.__total = "???"

    def __restore_btn_state(self):
        self.main_frame_control.execute_btn.config(
            text="开 始 处 理", bg=Theme.execute_btn_bg,
            command=self.main_frame_control.main, state='normal'
        )
        if self.__stop:
            messagebox.showinfo('提示', '程序已正常终止!')
        else:
            messagebox.showinfo('提示', '处理完成!')
        self.main_frame_control.overwrite_to_show_label("程序已终止!")
        SharedVariable.working = self.__stop = False

    def __execute_in_cmd(self):
        try:
            process = subprocess.Popen(
                'GFPGAN.py',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=False
            )

            self.main_frame_control.execute_btn.config(
                state='normal',
                command=self.set_stop_signal,
                bg=Theme.switch_frame_bg
            )

            for line in iter(process.stdout.readline, b''):
                if self.__stop:  # 如果收到了停止信号
                    process.terminate()  # 尝试正常终止进程
                    process.wait()  # 等待进程终止
                    break
                try:
                    decode_line = self.decode_output_text(line)
                    self.__update_progress(decode_line)
                    self.page_manager.dynamic_show_img_to_label()
                except Exception as e:
                    with open("Data/Error_log.txt", 'a', encoding='utf-8') as f:
                        f.write(f"{e}\n")
                    self.main_frame_control.overwrite_to_show_label('出现异常, 详见[帮助]中的[错误日志]!')
                    process.terminate()  # 出现异常，强制终止进程
                    process.wait()  # 等待进程终止
                    break  # 退出循环

            process.stdout.close()
            process.stderr.close()

        except Exception as e:
            with open("Data/Error_log.txt", 'a', encoding='utf-8') as f:
                f.write(f"执行外部程序时出现异常: {e}\n")

        finally:
            self.__restore_btn_state()

    def launch_main_thread(self):
        Thread(target=self.main).start()

    def main(self):
        if not path.exists("GFPGAN.py"):
            messagebox.showerror("错误", f"缺少文件: \n{path.abspath('GFPGAN.py')}")
            return
        self.main_frame_control.execute_btn.config(text='终 止 处 理', state='disabled', bg='#DB7058')
        messagebox.showinfo('提示', '开始处理!')
        self.main_frame_control.overwrite_to_show_label("启动模型程序中...")
        self.__execute_in_cmd()

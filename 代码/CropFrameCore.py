import zipfile
from tkinter import messagebox
from PIL import Image
from ImageApp import ImageApp
from SharedDatabase import SharedVariable, SendData
from time import perf_counter
from os import path, remove
from json import dump


class CropCore(object):
    # 裁剪人脸在计算放大比例时是基于固定的展示高度
    showFixedHeight = 407

    def __init__(self, crop_frame):
        self.crop_frame = crop_frame

    @staticmethod
    def __compress(img_path: str, json_data: list, outfile: str, showinfo=True):
        base_name, extension = path.splitext(path.basename(img_path))
        save_path = path.join(outfile, f'{base_name}.spg')
        temp_json_file = f'temp{perf_counter()}.json'
        temp_extension_file = f'temp{perf_counter()}.txt'
        with open(temp_json_file, 'w') as f:
            dump(json_data, f)
        with open(temp_extension_file, 'w')as f:
            f.write(extension[1:])
        with zipfile.ZipFile(save_path, 'w') as zipf:
            zipf.write(img_path, arcname='image')
            zipf.write(temp_json_file, arcname='json')
            zipf.write(temp_extension_file, arcname="ext")
        remove(temp_json_file)
        remove(temp_extension_file)
        messagebox.showinfo("提示", f"导出成功! 已保存在:\n{save_path}") if showinfo else 0
        return save_path

    def export(self, _, outfile=None, showinfo=True):
        outfile = self.get_export_path() if outfile is None else outfile
        if outfile is None:
            return
        img_path = self.crop_frame.main_canvas.get_current_img_path
        if img_path == "":
            return messagebox.showinfo("提示", "请选择要导出的图片!")
        coords = self.crop_frame.main_canvas.get_all_draw_coords
        if len(coords) == 0:
            ImageApp.copy_img_to_new_folder(img_path, outfile)
            messagebox.showinfo("提示", f"导出成功,已保存在:\n{outfile}中!") if showinfo else 0
            return path.join(outfile, path.basename(img_path))
        h = Image.open(img_path).size[1]
        expand_scale = self.__get_expand_scale(h)
        json_data = [[int(x * expand_scale) for x in sublist] for sublist in coords]
        return self.__compress(img_path, json_data, outfile, showinfo)

    def directly_add_to_task(self, _):
        img_path = self.crop_frame.main_canvas.get_current_img_path
        if img_path == "":
            return messagebox.showinfo("提示", "请选择要处理的图片!")
        if SharedVariable.working:
            self.export(0, SendData.infile, showinfo=False)
            SharedVariable.task_list.insert('end', path.basename(img_path))
            messagebox.showinfo("提示", "已加入任务列表!")
        else:
            result = SharedVariable.execute_entry()
            if not result:
                return
            export_path = self.export(0, SendData.infile, showinfo=False)
            SharedVariable.task_list.insert('end', path.basename(export_path))

    def get_export_path(self):
        outfile = self.crop_frame.export_entry.get()
        if outfile == "":
            messagebox.showinfo("提示", "请先选择文件导出路径!")
            return None
        if not path.isdir(outfile):
            messagebox.showinfo("错误", "文件导出路径不存在,\n请尝试重新输入!")
            return None
        return outfile

    @classmethod
    def __get_expand_scale(cls, orig_height) -> float:
        if orig_height < cls.showFixedHeight:
            return 1.0
        else:
            return orig_height / cls.showFixedHeight

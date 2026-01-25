"""
This file all base on the python standard library os, and make the most frequent operation set into a function,
to make the best use.
"""
import re
from PIL import Image
from os import scandir, path
from ImageApp import ImageApp
from tkinter import messagebox, filedialog


class FileJudgement(object):
    @classmethod
    def contains_img_or_folder(cls, folder_path):
        try:
            for file in scandir(folder_path):
                if path.isdir(file.path):
                    return True
                elif re.match(r".*?\.(jpg|jpeg|png)", file.name, re.I):
                    return True
            return False
        except (PermissionError, FileNotFoundError, NotADirectoryError):
            return False

    @classmethod
    def is_folder_name_error(cls, infile_path, outfile_path, extra_title=""):
        if infile_path == '' or outfile_path == '':
            messagebox.showinfo(f'{extra_title}提示', '文件输入或输出路径不能为空!')
            return True
        if not path.isdir(outfile_path) or not path.exists(infile_path):
            messagebox.showerror(f'{extra_title}错误', '输入或输出路径错误, 请检查路径!')
            return True
        if re.search(r'[\u4e00-\u9fff]', infile_path+outfile_path):
            messagebox.showerror(f'{extra_title}警告', '请不要在文件路径中包含中文!')
            return True
        return False

    @classmethod
    def ask_open_img(cls):
        file_types = (("Image files", "*.jpg *.png *.jpeg"),)
        img_path = filedialog.askopenfilename(filetypes=file_types)
        if not img_path:
            return False
        if not ImageApp.is_real_img(img_path):
            messagebox.showerror('错误', '无法识别该图片文件!')
            return False
        else:
            return img_path


class SpgManager(object):
    @classmethod
    def decompress_img(cls, spg_file) -> str:
        import zipfile
        from io import BytesIO
        try:
            with zipfile.ZipFile(spg_file, 'r') as zip_ref:
                img_data = zip_ref.read('image')
                extension = zip_ref.read("ext").decode("utf-8")
                image_bytes = BytesIO(img_data)
        except zipfile.error:
            return ""
        base_name = f"{path.basename(spg_file)[:-4]}.{extension}"
        save_path = path.join(path.dirname(spg_file), base_name)
        if not path.isfile(save_path):
            with Image.open(image_bytes) as img:
                img.save(save_path)
        return save_path

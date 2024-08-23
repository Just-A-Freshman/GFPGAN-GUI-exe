from PIL import Image, ImageTk, UnidentifiedImageError
from re import search
from os import path


class ImageApp(object):
    canvas_img_size = (65535, 411)
    thumbnail_size = (450, 246)

    @classmethod
    def create_thumbnail(cls, img_path=None):
        if img_path is None or not path.exists(img_path):
            return
        with Image.open(img_path) as img:
            img.thumbnail(cls.thumbnail_size)
            return ImageTk.PhotoImage(img)

    @classmethod
    def get_img_size(cls, img_path):
        img_size = path.getsize(img_path)
        if img_size < 1048576:
            img_size /= 1024
            return f'{img_size:.2f}KB'
        else:
            img_size /= (1024 * 1024)
            return f'{img_size:.2f}MB'

    @classmethod
    def change_palette_img(cls, canvas, img_path, judge_chinese=True):
        img = cls.is_real_img(img_path, judge_chinese)
        if not img:
            return
        img.thumbnail(cls.canvas_img_size)
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.configure(scrollregion=canvas.bbox('all'))
        return photo, img.width, img.height

    @staticmethod
    def copy_img_to_new_folder(old_img_path: str, new_folder_path: str):
        if not path.isdir(new_folder_path):
            raise UnidentifiedImageError
        base_name = path.basename(old_img_path)
        with Image.open(old_img_path) as img:
            img = img.copy()
            img.save(path.join(new_folder_path, base_name))

    @classmethod
    def is_real_img(cls, img_path, judge_chinese=True):
        if not path.isfile(img_path):
            return False
        base_name = path.basename(img_path)
        if search(r'[\u4e00-\u9fff]', base_name) and judge_chinese:
            return False
        if base_name.endswith("spg"):
            return True
        try:
            with Image.open(img_path).copy() as img:
                return img
        except UnidentifiedImageError:
            return False

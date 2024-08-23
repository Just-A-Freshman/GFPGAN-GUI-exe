import zipfile
from io import BytesIO
from PIL import Image
from os import path, makedirs


class Cropper(object):
    def __init__(self, outfile_path, expand_scale, real_ext, save_ext):
        self.outfile_path = outfile_path
        self.expand_scale = expand_scale
        self.real_ext = real_ext
        self.save_ext = save_ext
        self.image_bytes = b""
        self.basename = ""
        self.crop_dict = dict()

    def read_spg(self, spg_file):
        self.basename = path.basename(spg_file)[:-4]
        try:
            with zipfile.ZipFile(spg_file, 'r')as zip_ref:
                crop_coords = eval(zip_ref.read('json').decode("utf-8"))
                print(f"?<total:{len(crop_coords)}>")
                img_data = zip_ref.read('image')
        except zipfile.error:
            print(f"?<#bad:{spg_file}")
            return
        self.image_bytes = BytesIO(img_data)
        print("?<doing>")
        with Image.open(self.image_bytes) as img:
            makedirs(path.join(self.outfile_path, 'cropped_faces'), exist_ok=True)
            for idx, crop_loc in enumerate(crop_coords, 1):
                crop_img = img.crop(crop_loc)
                crop_basename = f'Man[{self.basename}]_{idx:02d}.png'
                crop_face = path.join(self.outfile_path, 'cropped_faces', crop_basename)
                crop_img.save(crop_face)
                self.crop_dict[crop_face] = [int(loc * self.expand_scale) for loc in crop_loc]
                decompress_img_path = path.join(path.dirname(spg_file), f"{self.basename}.{self.real_ext}")
            img.save(decompress_img_path)
            print("?<doing>")

    def paste_back(self):
        with Image.open(self.image_bytes) as img:
            old_w, old_h = img.size
            if self.expand_scale != 1:
                new_w, new_h = int(old_w * self.expand_scale), int(old_h * self.expand_scale)
                img = img.resize((new_w, new_h))
            print("?<doing>")
            for crop_face, coord in self.crop_dict.items():
                restore_face = path.join(self.outfile_path, 'restored_faces', path.basename(crop_face))
                with Image.open(restore_face)as deal_face:
                    img.paste(deal_face, coord)
            print("?<doing>")
            output_path = path.join(self.outfile_path, 'restored_images')
            save_path = path.join(output_path, f'{self.basename}.{self.save_ext}')
            makedirs(output_path, exist_ok=True)
            img.save(save_path)
            print(f'?<#done:{save_path}>')

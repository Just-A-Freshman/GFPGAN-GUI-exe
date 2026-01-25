import cv2
from os import path, makedirs
from numpy import concatenate
import builtins
from gfpgan import GFPGAN
from SharedDatabase import ReceiveData
from gfpgan_Crop import Cropper


def image_write(img, file_path, params=None, auto_mkdir=True):
    if auto_mkdir:
        dir_name = path.abspath(path.dirname(file_path))
        makedirs(dir_name, exist_ok=True)
    ok = cv2.imwrite(file_path, img, params)
    if not ok:
        raise IOError('Failed in writing images.')


class SuperResolution:
    def __init__(self):
        self.extension_dict = {"spg": "jpg", "speg": "jpeg", "sng": "png"}
        self.__expand_scale = 0
        self.__spg_file_real_ext = None
        self.__outfile = ""
        self.__out_format = ""
        self.receiver = ReceiveData()
        self.restorer = None
        self.cropped_faces = None
        self.restored_faces = None
        self.restored_img = None
        self.original_print = builtins.print
        builtins.print = self.unbuffered_print
        self.receiver.prefetching()
        print("?<#done>")
        self.allot_task_queue()

    def unbuffered_print(self, *args, **kwargs):
        kwargs['flush'] = True
        self.original_print(*args, **kwargs)

    def set_model(self, scale):
        # infile, in_format, outfile, out_format, expand_scale, basename
        model_path = 'gfpgan/weights/GFPGAN-v1.3.pth'
        self.restorer = GFPGAN(model_path=model_path, upscale=scale)

    def analysis_task(self):
        (infile, in_format, self.outfile, self.out_format,
         expand_scale, basename) = self.receiver.read_from_task()
        if infile == "":
            return None
        if in_format in self.extension_dict.keys():
            self.__spg_file_real_ext = self.extension_dict[in_format]
            infile_path = path.join(infile, f"{basename}.spg")
        else:
            infile_path = path.join(infile, f"{basename}.{in_format}")
        if expand_scale != self.__expand_scale:
            self.__expand_scale = expand_scale
            self.set_model(expand_scale)
        return infile_path

    def allot_task_queue(self):
        while True:
            self.__spg_file_real_ext = None
            infile_path = self.analysis_task()
            if infile_path is None:
                return
            if self.__spg_file_real_ext is not None:
                self.analysis_spg_file(infile_path)
            else:
                self.deal_face(infile_path)

    def analysis_spg_file(self, spg_file):
        print(f'?<start:{spg_file}>')
        cropper = Cropper(self.outfile, self.__expand_scale, self.__spg_file_real_ext, self.out_format)
        cropper.read_spg(spg_file)
        for crop_face in cropper.crop_dict.keys():
            cropped_face = cv2.imread(crop_face, cv2.IMREAD_COLOR)
            restored_face = self.restorer.enhance(cropped_face, show_progress=False)[2]
            print("?<doing>")
            restored_face_path = path.join(self.outfile, 'restored_faces', path.basename(crop_face))
            image_write(restored_face, restored_face_path)
            cropped_face = cv2.resize(cropped_face, restored_face.shape[1::-1], interpolation=cv2.INTER_LINEAR)
            cmp_img = concatenate((cropped_face, restored_face), axis=1)
            image_write(cmp_img, path.join(self.outfile, 'cmp', path.basename(crop_face)))
            print("?<doing>")
        cropper.paste_back()

    def deal_face(self, img_path):
        print(f'?<start:{img_path}>')
        input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        self.cropped_faces, self.restored_faces, self.restored_img = self.restorer.enhance(input_img)
        self.save_all(img_path)

    def save_all(self, img_path):
        print("?<doing>")
        basename = path.splitext(path.basename(img_path))[0]
        for idx, (cropped_face, restored_face) in enumerate(zip(self.cropped_faces, self.restored_faces)):
            # save cropped face
            save_crop_path = path.join(self.outfile, 'cropped_faces', f'{basename}_{idx:02d}.png')
            image_write(cropped_face, save_crop_path)
            # save restored face
            save_face_name = f'{basename}_{idx:02d}.png'
            save_restore_path = path.join(self.outfile, 'restored_faces', save_face_name)
            image_write(restored_face, save_restore_path)
            # save comparison image
            cmp_img = concatenate((cropped_face, restored_face), axis=1)
            image_write(cmp_img, path.join(self.outfile, 'cmp', f'{basename}_{idx:02d}.png'))
        print("?<doing>")
        save_path = path.join(self.outfile, "restored_images", f"{basename}.{self.out_format}")
        image_write(self.restored_img, save_path)
        print(f'?<#done:{img_path}>')


if __name__ == '__main__':
    s = SuperResolution()

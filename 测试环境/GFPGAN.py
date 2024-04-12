import cv2
import numpy as np
import builtins
from os import path, scandir, makedirs
from basicsr.utils import imwrite
from gfpgan import GFPGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer


class SuperResolution:
    def __init__(self):
        # 第一步，将GUI页面写入txt文件的数据导入
        self.infile = None
        self.outfile = None
        self.upscale: int = 2
        self.bg_tile: int = 400
        # self.suffix = None; This one is not important, so I just make it fixed.
        self.bg_tile: int = 400
        self.only_center_face: bool = False
        self.aligned: bool = False
        self.img_ext: str = 'auto'
        self.weight: float = 0.5
        self.img_list = []
        self.restorer = None
        self.cropped_faces = None
        self.restored_faces = None
        self.restored_img = None
        self.original_print = builtins.print
        builtins.print = self.unbuffered_print
        # 调用主函数
        self.main()

    def unbuffered_print(self, *args, **kwargs):
        kwargs['flush'] = True
        self.original_print(*args, **kwargs)

    def load_data(self):
        with open(f'load_data.txt', 'r', encoding='utf-8')as file:
            lines = file.readlines()
        self.infile = lines[0].strip()
        self.outfile = lines[1].strip()
        self.upscale = int(lines[2].strip()) if lines[2].strip() != '' else self.upscale
        self.bg_tile = int(lines[3].strip()) if lines[3].strip() != '' else self.bg_tile
        self.only_center_face = True if lines[4].strip() == '1' else self.only_center_face
        self.aligned = False if lines[5].strip() == '0' else self.aligned
        self.img_ext = lines[6].strip()
        self.weight = float(lines[7].strip())

    def deal_infile_path(self):
        if path.isfile(self.infile):
            self.img_list = [self.infile]
        else:
            self.img_list = [file.path for file in scandir(self.infile)]

        # 如果输出目录不存在就创建
        makedirs(self.outfile, exist_ok=True)

    def set_model(self):
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        bg_upsampler = RealESRGANer(
            scale=2,
            model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
            model=model,
            tile=self.bg_tile,
            tile_pad=10,
            pre_pad=0,
            half=False
        )

        model_path = 'experiments/pretrained_models/GFPGANv1.4.pth'
        self.restorer = GFPGANer(
            model_path=model_path,
            upscale=self.upscale,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=bg_upsampler)

    def deal_face(self):
        for img_path in self.img_list:
            # read image
            img_name = path.basename(img_path)
            print(f'正在处理图片[{img_name}]......')
            basename, ext = path.splitext(img_name)
            input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            print('正在读取图片信息......')
            # restore faces and background if necessary
            self.cropped_faces, self.restored_faces, self.restored_img = self.restorer.enhance(
                input_img,
                has_aligned=self.aligned,
                only_center_face=self.only_center_face,
                paste_back=True,
                weight=self.weight)

            self.save_face(basename, ext)

    def save_face(self, basename, ext):
        print('正在保存人脸照片......')
        for idx, (cropped_face, restored_face) in enumerate(zip(self.cropped_faces, self.restored_faces)):
            # save cropped face
            save_crop_path = path.join(self.outfile, 'cropped_faces', f'{basename}_{idx:02d}.png')
            imwrite(cropped_face, save_crop_path)
            # save restored face
            save_face_name = f'{basename}_{idx:02d}.png'
            save_restore_path = path.join(self.outfile, 'restored_faces', save_face_name)
            imwrite(restored_face, save_restore_path)
            # save comparison image
            cmp_img = np.concatenate((cropped_face, restored_face), axis=1)
            imwrite(cmp_img, path.join(self.outfile, 'cmp', f'{basename}_{idx:02d}.png'))
        self.save_restored_img(ext, basename)

    def save_restored_img(self, ext, basename):
        print('正在保存拼接图片......')
        if self.img_ext == 'auto':
            extension = ext[1:]
        else:
            extension = self.img_ext
        save_restore_path = path.join(self.outfile, 'restored_images', f'{basename}.{extension}')
        imwrite(self.restored_img, save_restore_path)
        print(f'图片处理完成，已保存在[{save_restore_path}]路径下!\n')

    def main(self):
        self.load_data()
        self.deal_infile_path()
        self.set_model()
        self.deal_face()


if __name__ == '__main__':
    s = SuperResolution()

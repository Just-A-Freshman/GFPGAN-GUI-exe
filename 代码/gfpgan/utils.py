from os import path
from torch import device as torch_device, load as torch_load, no_grad
from basicsr.utils import img2tensor, tensor2img
from facexlib.utils.face_restoration_helper import FaceRestoreHelper
from torchvision.transforms.functional import normalize
from gfpgan.archs.gfpganv1_clean_arch import GFPGANv1Clean
ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))


class GFPGAN:
    def __init__(self, model_path, upscale=2):
        self.upscale = upscale
        self.device = torch_device('cpu')
        self.gfpgan = GFPGANv1Clean(
            out_size=512,
            num_style_feat=512,
            channel_multiplier=2,
            decoder_load_path='',
            fix_decoder=False,
            num_mlp=8,
            input_is_latent=True,
            different_w=True,
            narrow=1,
            sft_half=True)
        # initialize face helper
        self.face_helper = FaceRestoreHelper(
            upscale,
            face_size=512,
            crop_ratio=(1, 1),
            det_model='retinaface_resnet50',
            save_ext='png',
            use_parse=True,
            device=self.device,
            model_rootpath='gfpgan/weights')

        load_net = torch_load(model_path)
        self.gfpgan.load_state_dict(load_net['params_ema'], strict=True)
        self.gfpgan.eval()
        self.gfpgan = self.gfpgan.to(self.device)

    @no_grad()
    def enhance(self, img, show_progress=True):
        self.face_helper.clean_all()
        self.face_helper.read_image(img)
        self.face_helper.get_face_landmarks_5(only_center_face=False, eye_dist_threshold=5)
        self.face_helper.align_warp_face()
        print(f"?<total:{len(self.face_helper.cropped_faces)}>") if show_progress else 0
        for cropped_face in self.face_helper.cropped_faces:
            print("?<doing>") if show_progress else 0
            cropped_face_t = img2tensor(cropped_face / 255., bgr2rgb=True, float32=True)
            normalize(cropped_face_t, [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], inplace=True)
            cropped_face_t = cropped_face_t.unsqueeze(0).to(self.device)
            try:
                output = self.gfpgan(cropped_face_t, return_rgb=False, weight=0.5)[0]
                # convert to image
                restored_face = tensor2img(output.squeeze(0), rgb2bgr=True, min_max=(-1, 1))
            except RuntimeError as error:
                print(f'?<##bad:Failed inference for GFPGAN: {error}.>')
                restored_face = cropped_face
            restored_face = restored_face.astype('uint8')
            self.face_helper.add_restored_face(restored_face)

        self.face_helper.get_inverse_affine(None)
        restored_img = self.face_helper.paste_faces_to_input_image(upsample_img=None, show_progress=show_progress)
        return self.face_helper.cropped_faces, self.face_helper.restored_faces, restored_img

import cv2
import onnxruntime
from PIL import Image
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def decode_image(im_file, im_info):
    """read rgb image
    Args:
        im_file (str/np.ndarray): path of image/ np.ndarray read by cv2
        im_info (dict): info of image
    Returns:
        im (np.ndarray):  processed image (np.ndarray)
        im_info (dict): info of processed image
    """
    if isinstance(im_file, str):
        with open(im_file, 'rb') as f:
            im_read = f.read()
        data = np.frombuffer(im_read, dtype='uint8')
        im = cv2.imdecode(data, 1)  # BGR mode, but need RGB mode
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im_info['origin_shape'] = im.shape[:2]
        im_info['resize_shape'] = im.shape[:2]
    else:
        # im = cv2.cvtColor(im_file, cv2.COLOR_BGR2RGB)
        im = im_file
        im_info['origin_shape'] = im.shape[:2]
        im_info['resize_shape'] = im.shape[:2]
    return im, im_info


def preprocess(im, preprocess_ops):
    # process image by preprocess_ops
    im_info = {
        'scale': [1., 1.],
        'origin_shape': None,
        'resize_shape': None,
        'pad_shape': None,
    }
    im, im_info = decode_image(im, im_info)
    for operator in preprocess_ops:
        im, im_info = operator(im, im_info)
    im = np.array((im,)).astype('float32')
    return im, im_info


class Permute(object):
    """permute image
    Args:
        to_bgr (bool): whether convert RGB to BGR
        channel_first (bool): whether convert HWC to CHW
    """

    def __init__(self, to_bgr=False, channel_first=True):
        self.to_bgr = to_bgr
        self.channel_first = channel_first

    def __call__(self, im, im_info):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
            im_info (dict): info of image
        Returns:
            im (np.ndarray):  processed image (np.ndarray)
            im_info (dict): info of processed image
        """
        if self.channel_first:
            im = im.transpose((2, 0, 1)).copy()
        if self.to_bgr:
            im = im[[2, 1, 0], :, :]
        return im, im_info


class Resize(object):
    """resize image by target_size and max_size
    Args:
        arch (str): model type
        target_size (int): the target size of image
        max_size (int): the max size of image
        use_cv2 (bool): whether us cv2
        image_shape (list): input shape of model
        interp (int): method of resize
    """

    def __init__(self,
                 arch,
                 target_size,
                 max_size,
                 use_cv2=True,
                 image_shape=None,
                 interp=cv2.INTER_LINEAR):
        self.target_size = target_size
        self.max_size = max_size
        self.image_shape = image_shape
        self.arch = arch
        self.use_cv2 = use_cv2
        self.interp = interp

    def __call__(self, im, im_info):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
            im_info (dict): info of image
        Returns:
            im (np.ndarray):  processed image (np.ndarray)
            im_info (dict): info of processed image
        """
        im_channel = im.shape[2]
        im_scale_x, im_scale_y = self.generate_scale(im)
        im_info['scale_factor'] = [[im_scale_y, im_scale_x]]
        im_info['resize_shape'] = [
            im_scale_x * float(im.shape[1]), im_scale_y * float(im.shape[0])
        ]
        if self.use_cv2:
            im = cv2.resize(im,
                            None,
                            None,
                            fx=im_scale_x,
                            fy=im_scale_y,
                            interpolation=self.interp)
        else:
            resize_w = int(im_scale_x * float(im.shape[1]))
            resize_h = int(im_scale_y * float(im.shape[0]))
            if self.max_size != 0:
                raise TypeError(
                    'If you set max_size to cap the maximum size of image,'
                    'please set use_cv2 to True to resize the image.')
            im = im.astype('uint8')
            im = Image.fromarray(im)
            im = im.resize((int(resize_w), int(resize_h)), self.interp)
            im = np.array(im)

        # padding im when image_shape fixed by infer_cfg.yml
        if self.max_size != 0 and self.image_shape is not None:
            padding_im = np.zeros((self.max_size, self.max_size, im_channel),
                                  dtype=np.float32)
            im_h, im_w = im.shape[:2]
            padding_im[:im_h, :im_w, :] = im
            im = padding_im

        return im, im_info

    def generate_scale(self, im):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
        Returns:
            im_scale_x: the resize ratio of X
            im_scale_y: the resize ratio of Y
        """
        origin_shape = im.shape[:2]
        im_scale_x = float(self.target_size[1]) / float(origin_shape[1])
        im_scale_y = float(self.target_size[0]) / float(origin_shape[0])
        return im_scale_x, im_scale_y


class Normalize(object):
    """normalize image
    Args:
        mean (list): im - mean
        std (list): im / std
        is_scale (bool): whether need im / 255
        is_channel_first (bool): if True: image shape is CHW, else: HWC
    """

    def __init__(self, mean, std, is_scale=True, is_channel_first=False):
        self.mean = mean
        self.std = std
        self.is_scale = is_scale
        self.is_channel_first = is_channel_first

    def __call__(self, im, im_info):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
            im_info (dict): info of image
        Returns:
            im (np.ndarray):  processed image (np.ndarray)
            im_info (dict): info of processed image
        """
        im = im.astype(np.float32, copy=False)
        if self.is_channel_first:
            mean = np.array(self.mean)[:, np.newaxis, np.newaxis]
            std = np.array(self.std)[:, np.newaxis, np.newaxis]
        else:
            mean = np.array(self.mean)[np.newaxis, np.newaxis, :]
            std = np.array(self.std)[np.newaxis, np.newaxis, :]
        if self.is_scale:
            im = im / 255.0
        im -= mean
        im /= std
        return im, im_info


class Detector(object):
    """
    Args:
        config (object): config of model, defined by `Config(model_dir)`
        model_dir (str): root path of __model__, __params__ and infer_cfg.yml
        use_gpu (bool): whether use gpu
        run_mode (str): mode of running(fluid/trt_fp32/trt_fp16)
        threshold (float): threshold to reserve the result for output.
    """

    def __init__(self, model_dir):
        self.session = onnxruntime.InferenceSession(model_dir)

        self.input_names = [input.name for input in self.session.get_inputs()]
        self.output_names = [output.name for output in self.session.get_outputs()]

    def preprocess(self, im):
        preprocess_ops = []

        for op_info in [{'interp': 2, 'target_size': [416, 416], 'type': 'Resize'},
                        {'is_scale': True, 'mean': [0.5, 0.5, 0.5], 'std': [0.5, 0.5, 0.5],
                         'type': 'Normalize'},
                        {'type': 'Permute'}]:
            new_op_info = op_info.copy()
            op_type = new_op_info.pop('type')

            if op_type == 'Resize':
                new_op_info['arch'] = 'PicoDet'
                new_op_info['max_size'] = 0

            preprocess_ops.append(eval(op_type)(**new_op_info))
        im, im_info = preprocess(im, preprocess_ops)
        inputs = {'image': im}

        return inputs, im_info

    def predict(self, image):
        '''
        Args:
            image (str/np.ndarray): path of image/ np.ndarray read by cv2
            threshold (float): threshold of predicted box' score
        Returns:
            results (dict): include 'boxes': np.ndarray: shape:[N,6], N: number of box,
                            matix element:[class, score, x_min, y_min, x_max, y_max]
                            MaskRCNN's results include 'masks': np.ndarray:
                            shape:[N, class_num, mask_resolution, mask_resolution]
        '''
        inputs, im_info = self.preprocess(image)
        np_boxes, np_cls = self.session.run(self.output_names, inputs)

        return np_boxes[0, :, :], np_cls[0, :, :].T, im_info["scale_factor"][0]


class OnnxInfer():
    def __init__(self, model_path):
        self.detector = Detector(model_path)

        self.label_dic = {0: 'Fifth Distal Phalange_0', 1: 'Fifth Distal Phalange_1', 2: 'Fifth Distal Phalange_2',
                          3: 'Fifth Distal Phalange_3', 4: 'Fifth Distal Phalange_4', 5: 'Fifth Distal Phalange_5',
                          6: 'Fifth Distal Phalange_6', 7: 'Fifth Distal Phalange_7', 8: 'Fifth Distal Phalange_8',
                          9: 'Fifth Distal Phalange_9', 10: 'Fifth Distal Phalange_10', 11: 'Fifth Distal Phalange_11',
                          12: 'Fifth Metacarpal_0', 13: 'Fifth Metacarpal_1', 14: 'Fifth Metacarpal_2',
                          15: 'Fifth Metacarpal_3', 16: 'Fifth Metacarpal_4', 17: 'Fifth Metacarpal_5',
                          18: 'Fifth Metacarpal_6', 19: 'Fifth Metacarpal_7', 20: 'Fifth Metacarpal_8',
                          21: 'Fifth Metacarpal_9', 22: 'Fifth Metacarpal_10', 23: 'Fifth Middle Phalange_0',
                          24: 'Fifth Middle Phalange_1', 25: 'Fifth Middle Phalange_2', 26: 'Fifth Middle Phalange_3',
                          27: 'Fifth Middle Phalange_4', 28: 'Fifth Middle Phalange_5', 29: 'Fifth Middle Phalange_6',
                          30: 'Fifth Middle Phalange_7', 31: 'Fifth Middle Phalange_8', 32: 'Fifth Middle Phalange_9',
                          33: 'Fifth Middle Phalange_10', 34: 'Fifth Middle Phalange_11', 35: 'Fifth Middle Phalange_12',
                          36: 'Fifth Proximal Phalange_0', 37: 'Fifth Proximal Phalange_1',
                          38: 'Fifth Proximal Phalange_2', 39: 'Fifth Proximal Phalange_3',
                          40: 'Fifth Proximal Phalange_4', 41: 'Fifth Proximal Phalange_5',
                          42: 'Fifth Proximal Phalange_6', 43: 'Fifth Proximal Phalange_7',
                          44: 'Fifth Proximal Phalange_8', 45: 'Fifth Proximal Phalange_9',
                          46: 'Fifth Proximal Phalange_10', 47: 'Fifth Proximal Phalange_11',
                          48: 'Fifth Proximal Phalange_12', 49: 'First Distal Phalange_0',
                          50: 'First Distal Phalange_1', 51: 'First Distal Phalange_2',
                          52: 'First Distal Phalange_3', 53: 'First Distal Phalange_4',
                          54: 'First Distal Phalange_5', 55: 'First Distal Phalange_6',
                          56: 'First Distal Phalange_7', 57: 'First Distal Phalange_8',
                          58: 'First Distal Phalange_9', 59: 'First Distal Phalange_10',
                          60: 'First Distal Phalange_11', 61: 'First Metacarpal_0',
                          62: 'First Metacarpal_1', 63: 'First Metacarpal_2', 64: 'First Metacarpal_3',
                          65: 'First Metacarpal_4', 66: 'First Metacarpal_5', 67: 'First Metacarpal_6',
                          68: 'First Metacarpal_7', 69: 'First Metacarpal_8', 70: 'First Metacarpal_9',
                          71: 'First Metacarpal_10', 72: 'First Metacarpal_11', 73: 'First Proximal Phalange_0',
                          74: 'First Proximal Phalange_1', 75: 'First Proximal Phalange_2',
                          76: 'First Proximal Phalange_3', 77: 'First Proximal Phalange_4',
                          78: 'First Proximal Phalange_5', 79: 'First Proximal Phalange_6',
                          80: 'First Proximal Phalange_7', 81: 'First Proximal Phalange_8',
                          82: 'First Proximal Phalange_9', 83: 'First Proximal Phalange_10',
                          84: 'First Proximal Phalange_11', 85: 'First Proximal Phalange_12',
                          86: 'Radius_0', 87: 'Radius_1', 88: 'Radius_2', 89: 'Radius_3', 90: 'Radius_4',
                          91: 'Radius_5', 92: 'Radius_6', 93: 'Radius_7', 94: 'Radius_8', 95: 'Radius_9',
                          96: 'Radius_10', 97: 'Radius_11', 98: 'Radius_12', 99: 'Radius_13', 100: 'Radius_14',
                          101: 'Third Distal Phalange_0', 102: 'Third Distal Phalange_1',
                          103: 'Third Distal Phalange_2', 104: 'Third Distal Phalange_3',
                          105: 'Third Distal Phalange_4', 106: 'Third Distal Phalange_5',
                          107: 'Third Distal Phalange_6', 108: 'Third Distal Phalange_7',
                          109: 'Third Distal Phalange_8', 110: 'Third Distal Phalange_9',
                          111: 'Third Distal Phalange_10', 112: 'Third Distal Phalange_11', 113: 'Third Metacarpal_0',
                          114: 'Third Metacarpal_1', 115: 'Third Metacarpal_2', 116: 'Third Metacarpal_3',
                          117: 'Third Metacarpal_4', 118: 'Third Metacarpal_5', 119: 'Third Metacarpal_6',
                          120: 'Third Metacarpal_7', 121: 'Third Metacarpal_8', 122: 'Third Metacarpal_9',
                          123: 'Third Metacarpal_10', 124: 'Third Middle Phalange_0', 125: 'Third Middle Phalange_1',
                          126: 'Third Middle Phalange_2', 127: 'Third Middle Phalange_3',
                          128: 'Third Middle Phalange_4', 129: 'Third Middle Phalange_5',
                          130: 'Third Middle Phalange_6', 131: 'Third Middle Phalange_7',
                          132: 'Third Middle Phalange_8', 133: 'Third Middle Phalange_9',
                          134: 'Third Middle Phalange_10', 135: 'Third Middle Phalange_11',
                          136: 'Third Middle Phalange_12', 137: 'Third Proximal Phalange_0',
                          138: 'Third Proximal Phalange_1', 139: 'Third Proximal Phalange_2',
                          140: 'Third Proximal Phalange_3', 141: 'Third Proximal Phalange_4',
                          142: 'Third Proximal Phalange_5', 143: 'Third Proximal Phalange_6',
                          144: 'Third Proximal Phalange_7', 145: 'Third Proximal Phalange_8',
                          146: 'Third Proximal Phalange_9', 147: 'Third Proximal Phalange_10',
                          148: 'Third Proximal Phalange_11', 149: 'Third Proximal Phalange_12',
                          150: 'Ulna_0', 151: 'Ulna_1', 152: 'Ulna_2', 153: 'Ulna_3', 154: 'Ulna_4',
                          155: 'Ulna_5', 156: 'Ulna_6', 157: 'Ulna_7', 158: 'Ulna_8', 159: 'Ulna_9',
                          160: 'Ulna_10', 161: 'Ulna_11', 162: 'Ulna_12'}

    def convert(self, size, box):
        dw = 1. / size[1]
        dh = 1. / size[0]
        x = (box[0] + box[2]) / 2.0
        y = (box[1] + box[3]) / 2.0
        w = box[2] - box[0]
        h = box[3] - box[1]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        box = [x, y, w, h]
        return box

    def do_infer(self, img_path, conf=0.1):
        img = cv2.imread(img_path)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        size = image.shape[0:2]
        results_box, results_cls, results_scale = self.detector.predict(image=image)
        only_dic = {}
        for list_idx, result in enumerate(results_cls):
            cls_score = result.tolist()
            score = max(cls_score)
            if score > conf:
                label_num = cls_score.index(score)
                label_name = self.label_dic[int(label_num)]
                bone_name, bone_level = label_name.split('_')
                if bone_name not in only_dic:
                    out_box = list(results_box[list_idx])
                    out_box[0] = out_box[0] / results_scale[1]
                    out_box[1] = out_box[1] / results_scale[0]
                    out_box[2] = out_box[2] / results_scale[1]
                    out_box[3] = out_box[3] / results_scale[0]
                    box = self.convert(size,out_box)
                    only_dic[bone_name] = {'level': bone_level, 'score': score, 'box': box}
                elif score >= only_dic[bone_name]['score']:
                    out_box = list(results_box[list_idx])
                    out_box[0] = out_box[0] / results_scale[1]
                    out_box[1] = out_box[1] / results_scale[0]
                    out_box[2] = out_box[2] / results_scale[1]
                    out_box[3] = out_box[3] / results_scale[0]
                    box = self.convert(size, out_box)
                    only_dic[bone_name] = {'level': bone_level, 'score': score, 'box': box}

        return only_dic


if __name__ == '__main__':
    model_path = 'Model_rus_chn.onnx'
    model = OnnxInfer(model_path)
    img_in = 'E:/infer_ml/data/test/images/2802.png'
    output = model.do_infer(img_in)

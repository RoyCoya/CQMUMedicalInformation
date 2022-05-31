import os
import cv2
from torch import nn
import torch
from PIL import Image
from torchvision import transforms
from .model import swin_tiny_patch4_window7_224 as create_model
import numpy as np

class BoneGrade(object):
    def __init__(self, weights_path, img_size):
        self.weights_cls = {'First Distal Phalange': 12,
                            'Fifth Metacarpal': 11,
                            'Fifth Middle Phalange': 13,
                            'Fifth Proximal Phalange': 13,
                            'Fifth Distal Phalange': 12,
                            'First Metacarpal': 12,
                            'First Proximal Phalange': 13,
                            'Radius': 15,
                            'Third Distal Phalange': 12,
                            'Third Metacarpal': 11,
                            'Third Middle Phalange': 13,
                            'Third Proximal Phalange': 13,
                            'Ulna': 13}

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.swinT = create_model(num_classes=15).to(self.device)
        self.weights_path = weights_path
        self.img_size = img_size

    def pre_gray(self, image, weight_name):
        # [N, C, H, W]
        data_transform = transforms.Compose(
            [transforms.Resize(int(self.img_size)),
             transforms.ToTensor(),
             ])
        image = Image.fromarray(np.uint8(image))
        image = data_transform(image)
        # expand batch dimension
        image = torch.unsqueeze(image, dim=0)
        # 更换最后一层 输出头
        num_classes = self.weights_cls[weight_name]
        head_in_features = self.swinT.head.in_features
        self.swinT.head = nn.Linear(head_in_features, num_classes).to(self.device)
        # load model weights
        weight_path = os.path.join(self.weights_path, weight_name)
        self.swinT.load_state_dict(torch.load(weight_path, map_location=self.device))
        self.swinT.eval()
        with torch.no_grad():
            # predict class
            pre_grade = torch.softmax(torch.squeeze(self.swinT(image.to(self.device)).to(self.device)), dim=0)
            predict_cla = torch.argmax(pre_grade).cpu().numpy()
        return int(predict_cla)




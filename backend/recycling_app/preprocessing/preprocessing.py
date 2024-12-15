from torchvision.transforms import v2
import torch
from typing import Union
from io import BytesIO
from PIL import Image


class Preprocessor:

    def __init__(self) -> None:
        self.transform_train = v2.Compose(
            [
                v2.ToImage(),
                v2.Lambda(lambda x: self.remove_alpha(x)),
                v2.ToDtype(torch.uint8, scale=True),
                v2.Grayscale(num_output_channels=3),
                v2.GaussianBlur(kernel_size=5, sigma=(0.1, 2.0)),
                v2.RandomRotation(degrees=(0, 360)),
                v2.RandomResizedCrop(size=(224, 224), scale=(0.3, 1), antialias=True),
                v2.ToDtype(torch.float32, scale=True),
                v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )
        self.transform_test = v2.Compose(
            [
                v2.ToImage(),
                v2.Lambda(lambda x: self.remove_alpha(x)),
                v2.ToDtype(torch.uint8, scale=True),
                v2.Grayscale(num_output_channels=3),
                v2.Resize(size=(224, 224), antialias=True),
                v2.ToDtype(torch.float32, scale=True),
                v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )
    
    def remove_alpha(self, img, background_color=(255, 255, 255)):
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            background = Image.new("RGB", img.size, background_color)
            background.paste(img, mask=img.getchannel("A"))  # Nakładanie z kanałem alfa
            return background
        else:
            return img.convert("RGB")

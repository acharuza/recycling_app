from torchvision.transforms import v2
from PIL import Image
import torch
from io import BytesIO
from typing import Union


class Preprocessor:

    def __init__(self) -> None:
        self.transform = v2.Compose(
            [
                v2.ToImage(),
                v2.ToDtype(torch.uint8, scale=True),
                v2.Grayscale(num_output_channels=3),
                v2.GaussianBlur(kernel_size=5, sigma=(0.1, 2.0)),
                v2.RandomRotation(degrees=(0, 360)),
                v2.RandomResizedCrop(size=(224, 224), scale=(0.3, 1), antialias=True),
                v2.ToDtype(torch.float32, scale=True),
                v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

    # def __call__(self, image: Union[str, Image.Image, BytesIO]) -> torch.Tensor:
    #     if isinstance(image, str):
    #         image = self.__load_image_from_path(image)
    #     elif isinstance(image, BytesIO):
    #         image = self.__load_image_from_memory(image)
    #     transformed_img = self.transform(image)
    #     return transformed_img

    # def __load_image_from_path(self, image_path: str) -> Image.Image:
    #     return Image.open(image_path)

    # def __load_image_from_memory(self, image_data: BytesIO) -> Image.Image:
    #     return Image.open(image_data)

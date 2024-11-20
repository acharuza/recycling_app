from torchvision.transforms import v2
from PIL import Image
import torch


class Preprocessor:

    def __init__(self) -> None:
        self.transform = v2.Compose(
            [
                v2.ToImage(),
                v2.ToDtype(torch.uint8, scale=True),
                v2.Grayscale(num_output_channels=3),
                v2.GaussianBlur(kernel_size=5, sigma=(0.1, 2.0)),
                v2.RandomResizedCrop(size=(224, 224), scale=(0.3, 1), antialias=True),
                v2.RandomRotation(degrees=(0, 360)),
                v2.ToDtype(torch.float32, scale=True),
                v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

    def __call__(self, image_path: str) -> torch.Tensor:
        image = self.__load_image(image_path)
        transformed_img = self.transform(image)
        return transformed_img

    def __load_image(self, image_path: str) -> Image:
        return Image.open(image_path)

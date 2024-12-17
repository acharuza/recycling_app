from torchvision import datasets
from recycling_app.preprocessing.preprocessing import Preprocessor
from torch.utils.data import DataLoader, random_split
from torch import Generator


def create_data_loaders(
    dataset_path: str,
    batch_size: int,
    seed: int,
    preprocessor: Preprocessor,
    split_ratio: float = 0.8,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    dataset = datasets.ImageFolder(dataset_path)
    train_size, val_size, test_size = _calculate_sizes(dataset, split_ratio)
    train_dataset, val_dataset, test_dataset = _split_train_val_test(
        dataset, train_size, val_size, test_size, seed
    )

    train_dataset.dataset.transform = preprocessor.transform_train
    val_dataset.dataset.transform = preprocessor.transform_test
    test_dataset.dataset.transform = preprocessor.transform_test

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, test_loader, dataset


def _calculate_sizes(
    dataset: datasets.ImageFolder, split_ratio: float
) -> tuple[int, int, int]:
    test_size = int((1 - split_ratio) * len(dataset))
    train_val_size = len(dataset) - test_size
    train_size = int(split_ratio * train_val_size)
    val_size = train_val_size - train_size
    return train_size, val_size, test_size


def _split_train_val_test(
    dataset: datasets.ImageFolder,
    train_size: int,
    val_size: int,
    test_size: int,
    seed: int,
) -> tuple[datasets.ImageFolder, datasets.ImageFolder, datasets.ImageFolder]:
    generator = Generator().manual_seed(seed)
    train_dataset, val_dataset, test_dataset = random_split(
        dataset, [train_size, val_size, test_size], generator=generator
    )
    return train_dataset, val_dataset, test_dataset

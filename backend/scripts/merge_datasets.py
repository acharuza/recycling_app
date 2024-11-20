import os
import shutil

DATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)


def _create_directories(data_dirs: list) -> None:
    path = DATA_DIRECTORY
    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, "raw"), exist_ok=True)
    os.makedirs(os.path.join(path, "processed"), exist_ok=True)
    for data_dir in data_dirs:
        for dir in os.listdir(data_dir):
            if os.path.isdir(os.path.join(data_dir, dir)):
                os.makedirs(
                    _extract_category(
                        os.path.join(data_dir, dir), os.path.join(path, "raw")
                    ),
                    exist_ok=True,
                )
                os.makedirs(
                    _extract_category(
                        os.path.join(data_dir, dir), os.path.join(path, "processed")
                    ),
                    exist_ok=True,
                )


def _extract_category(directory_path: str, destination_path: str) -> str:
    new_path = os.path.join(
        destination_path,
        os.path.basename(directory_path)
        .lower()
        .replace(" trash", "")
        .replace("miscellaneous", "trash")
        .replace(" ", "_"),
    )
    return new_path


def _move_files(data_dirs: list) -> None:
    for data_dir in data_dirs:
        for dir in os.listdir(data_dir):
            dir_path = os.path.join(data_dir, dir)
            if os.path.isdir(dir_path):
                new_path = _extract_category(
                    os.path.join(data_dir, dir), os.path.join(DATA_DIRECTORY, "raw")
                )

                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)

                    if os.path.isfile(file_path):
                        new_file_name = f"{os.path.basename(data_dir)}_{file_name}"
                        new_file_path = os.path.join(new_path, new_file_name)
                        shutil.copy(file_path, new_file_path)


def merge_datasets(data_dirs: list):
    _create_directories(data_dirs)
    _move_files(data_dirs)


if __name__ == "__main__":
    # tutaj trzeba podać ścieżki do folderów z danymi
    data_dirs = [
        os.path.join(
            DATA_DIRECTORY,
            "RealWaste",
        ),
        os.path.join(
            DATA_DIRECTORY,
            "Garbage classification",
        ),
    ]
    merge_datasets(data_dirs)

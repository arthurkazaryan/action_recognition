from argparse import ArgumentParser

from utils import DatasetPathsData

if __name__ == "__main__":
    parser = ArgumentParser()
    # parser.add_argument()

    dataset_paths_data = DatasetPathsData()
    if not dataset_paths_data.archive_path.is_file():
        dataset_paths_data.download_dataset()
    if not dataset_paths_data.archive_folder.native.is_dir():
        dataset_paths_data.extract_dataset()

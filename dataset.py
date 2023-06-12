from argparse import ArgumentParser

import pandas as pd
from tqdm import tqdm
from pytube import YouTube

from settings import YOUTUBE_VIDEO_URL
from utils import DatasetPathsData, logger

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--subset", help="Train/val samples to download", default="train")
    parser.add_argument("-n", "--number", help="Number of samples to download", default=None)
    args = parser.parse_args()

    dataset_paths_data = DatasetPathsData()
    if not dataset_paths_data.archive_path.is_file():
        logger.info(f"Downloading dataset to {dataset_paths_data.archive_path}")
        dataset_paths_data.download_dataset()
    if not dataset_paths_data.archive_folder.native.is_dir():
        logger.info(f"Extracting dataset to {dataset_paths_data.archive_folder.native}")
        dataset_paths_data.extract_dataset()

    csv_path = getattr(dataset_paths_data.archive_folder, args.subset)
    csv_path_subset = csv_path.with_name(args.subset + "_dance.csv")
    if not csv_path_subset.is_file():
        df = pd.read_csv(csv_path)
        df = df[df.label.str.contains("dancing")]
        df['path'] = None
        df.to_csv(csv_path_subset, index=False)
    else:
        df = pd.read_csv(csv_path_subset)
        df = df[~df["path"].notnull()]

    download_folder = dataset_paths_data.native.joinpath(args.subset)
    total_num = int(args.number) if args.number else len(df)
    df_subsample = df.sample(total_num)

    for index, row in tqdm(df_subsample.iterrows(), total=total_num):
        try:
            youtube_obj = YouTube(YOUTUBE_VIDEO_URL.format(row["youtube_id"]))
            file_path = download_folder.joinpath(youtube_obj.streams.first().default_filename)
            if not file_path.is_file():
                youtube_obj.streams.first().download(download_folder)
            df.loc[index, "path"] = str(file_path)
        except Exception as e:
            logger.warning(str(e))

    df.to_csv(csv_path_subset, index=False)

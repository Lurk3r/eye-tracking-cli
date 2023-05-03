import os
import pandas as pd
from tqdm import tqdm
import data_process_function as dpf
import time
import glob


def read_data(path):
    return pd.read_csv(path, sep='\t', low_memory=False)


def process_tsv_files(directory):
    tsv_files = glob.glob(os.path.join(directory, '*.tsv'))
    wait_for_concat_list = []

    for tsv_file in tqdm(tsv_files):
        tsv_path = os.path.join(directory, tsv_file)

        data = read_data(tsv_path)
        output_files = (
            dpf.calculate_fixation_count(data),
            dpf.calculate_duration_count(data),
            dpf.calculate_duration_mean(data),
            dpf.calculate_pupil_diameter_mean(data),
            dpf.calculate_pupil_diameter_max(data),
            dpf.calculate_pupil_diameter_min(data)
        )
        output_file = pd.concat(output_files, axis=1, join='inner')
        wait_for_concat_list.append(output_file)

    output_file_path = os.path.join(directory, 'stimulus_base_metric.csv')
    output_file = pd.concat(wait_for_concat_list)
    output_file.to_csv(output_file_path, encoding='utf-8-sig')


def process_tsv_files_aoi(directory):
    tsv_files = glob.glob(os.path.join(directory, '*.tsv'))

    # Initialize empty data frames for each output
    fixation_count_df = pd.DataFrame()
    duration_count_df = pd.DataFrame()
    duration_mean_df = pd.DataFrame()

    # Loop through all TSV files and process them
    for tsv_file in tqdm(tsv_files):
        tsv_path = os.path.join(directory, tsv_file)

        data = read_data(tsv_path)
        output_files = [
            dpf.calculate_fixation_count_aoi(data),
            dpf.calculate_duration_count_aoi(data),
            dpf.calculate_duration_mean_aoi(data)
        ]

        # Add the output of each calculation to the corresponding data frame
        fixation_count_df = pd.concat(
            [fixation_count_df, output_files[0]], axis=0)
        duration_count_df = pd.concat(
            [duration_count_df, output_files[1]], axis=0)
        duration_mean_df = pd.concat(
            [duration_mean_df, output_files[2]], axis=0)

    # Save the data frames to CSV files
    fixation_count_df.to_csv(os.path.join(
        directory, 'stimulus_aoi_fixation_count.csv'), encoding='utf-8-sig')
    duration_count_df.to_csv(os.path.join(
        directory, 'stimulus_aoi_duration_count.csv'), encoding='utf-8-sig')
    duration_mean_df.to_csv(os.path.join(
        directory, 'stimulus_aoi_duration_mean.csv'), encoding='utf-8-sig')


if __name__ == '__main__':
    print('请在下方输入包含tsv文件的文件夹路径，按下Enter键开始处理：')
    directory = input().strip()
    print(f'您输入的文件夹路径为：{directory}')
    if not os.path.exists(directory):
        print(f'无效的文件夹路径：{directory}，程序将退出。')
        time.sleep(5)
        exit()
    print('请耐心等待进度条走完')
    print('正在计算基于区间的指标：')
    process_tsv_files(directory)
    print('正在计算基于区间&AOI的指标：')
    process_tsv_files_aoi(directory)
    print('请检查文件，确保无误。应用将在10s后退出')
    time.sleep(10)

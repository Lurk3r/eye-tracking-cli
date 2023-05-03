# 1. 这一部分主要计算区间的fixation总数、duration的总和，平均duration
import numpy as np


def calculate_fixation_count(df):
    result = (df[df['Eye movement type'] == 'Fixation'].groupby(['Presented Stimulus name', 'Participant name'])
              ['Eye movement type index'].agg(lambda x: x.max() - x.min() + 1)
              .astype(int)
              .reset_index())
    result.columns = ['Presented Stimulus name',
                      'Participant name', 'Fixation count']
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_duration_count(df):
    result = (df[df['Eye movement type'] == 'Fixation'].groupby(['Presented Stimulus name', 'Participant name', 'Eye movement type index'])['Gaze event duration'].unique()
              .apply(lambda x: np.sum(x))
              .groupby(['Presented Stimulus name', 'Participant name'])
              .sum()
              .astype(int)
              .reset_index())
    result.columns = ['Presented Stimulus name',
                      'Participant name', 'Count duration']
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_duration_mean(df):
    result = (df[df['Eye movement type'] == 'Fixation'].groupby(['Presented Stimulus name', 'Participant name', 'Eye movement type index'])['Gaze event duration'].unique()
              .apply(lambda x: np.sum(x))
              .groupby(['Presented Stimulus name', 'Participant name'])
              .mean()
              .round(3)  # 保留三位小数
              .astype(float)
              .reset_index())
    result.columns = ['Presented Stimulus name',
                      'Participant name', 'Mean duration']
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_pupil_diameter_mean(df):
    result = (df.groupby(['Presented Stimulus name', 'Participant name'])[['Pupil diameter left', 'Pupil diameter right']]
              .mean()
              .astype(float)
              .reset_index())
    result['pupil diameter mean'] = result[['Pupil diameter left',
                                            'Pupil diameter right']].mean(axis=1).round(3)  # 新增一个计算平均值的步骤
    result.drop(['Pupil diameter left', 'Pupil diameter right'],
                axis=1, inplace=True)  # 删除原有的字段
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_pupil_diameter_max(df):
    result = (df.groupby(['Presented Stimulus name', 'Participant name'])[['Pupil diameter left', 'Pupil diameter right']]
              .max()
              .astype(float)
              .reset_index())
    result['pupil diameter max'] = result[['Pupil diameter left',
                                           'Pupil diameter right']].max(axis=1).round(3)  # 新增一个计算平均值的步骤
    result.drop(['Pupil diameter left', 'Pupil diameter right'],
                axis=1, inplace=True)  # 删除原有的字段
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_pupil_diameter_min(df):
    result = (df.groupby(['Presented Stimulus name', 'Participant name'])[['Pupil diameter left', 'Pupil diameter right']]
              .min()
              .astype(float)
              .reset_index())
    result['pupil diameter min'] = result[['Pupil diameter left',
                                           'Pupil diameter right']].min(axis=1).round(3)  # 新增一个计算平均值的步骤
    result.drop(['Pupil diameter left', 'Pupil diameter right'],
                axis=1, inplace=True)  # 删除原有的字段
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_fixation_count_aoi(df):
    result = (df[df['Eye movement type'] == 'Fixation'].groupby(['Presented Stimulus name', 'Participant name', 'Ungrouped'])
              ['Eye movement type index'].agg(lambda x: x.max() - x.min() + 1)
              .astype(int)
              .reset_index())
    result.columns = ['Presented Stimulus name',
                      'Participant name', 'Aoi type', 'Aoi fixation count']
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_duration_count_aoi(df):
    result = (df[df['Eye movement type'] == 'Fixation']
              .groupby(['Presented Stimulus name', 'Participant name', 'Ungrouped', 'Eye movement type index'])['Gaze event duration']
              .unique()
              .apply(lambda x: x[0])
              .reset_index()
              .groupby(['Presented Stimulus name', 'Participant name', 'Ungrouped'])['Gaze event duration']
              .sum()
              .astype(int)
              .reset_index())

    result.columns = ['Presented Stimulus name',
                      'Participant name', 'Ungrouped', 'Aoi duration sum']
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result


def calculate_duration_mean_aoi(df):
    result = (df[df['Eye movement type'] == 'Fixation']
              .groupby(['Presented Stimulus name', 'Participant name', 'Ungrouped', 'Eye movement type index'])['Gaze event duration']
              .unique()
              .apply(lambda x: x[0])
              .reset_index()
              .groupby(['Presented Stimulus name', 'Participant name', 'Ungrouped'])['Gaze event duration']
              .mean()
              .round(3)
              .astype(float)
              .reset_index())

    result.columns = ['Presented Stimulus name',
                      'Participant name', 'Ungrouped', 'Aoi duration mean']
    result.set_index(['Presented Stimulus name',
                     'Participant name'], inplace=True)
    return result

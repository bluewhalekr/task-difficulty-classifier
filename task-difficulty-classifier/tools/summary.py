from collections import Counter
import io

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_instance_count(df, columns):
    cnt = Counter()
    for f_instances in df[columns]:
        for inst in f_instances:
            cnt[inst] += 1
    df_instance = pd.DataFrame(cnt, index=['Count']).T.sort_values(by='Count', ascending=False)
    df_instance['Percentage'] = np.round(df_instance['Count'] / df_instance['Count'].sum(axis=0), 3)
    
    return df_instance


def get_folder_analysis(df):
    n_files = df.groupby('folder')[['difficulty']].count().reset_index().rename(columns={'difficulty':'n_file'})
    n_instances = df.groupby('folder')[['n_instance']].sum().reset_index()
    avg_size_occlusion = df.groupby('folder')[['avg_size_ratio', 'avg_n_occlusion']].mean().reset_index()
    df_folder = pd.merge(n_files, n_instances, how='left', on='folder')
    df_folder = pd.merge(df_folder, avg_size_occlusion, how='left', on='folder')

    return df_folder


def get_agg_table(df, column, groupby=None):
    if groupby:
        agg_table = df.groupby(groupby)[column].describe()[['min', '25%', '50%', '75%', 'max', 'mean']].T[['low', 'intermediate', 'high']]
    else:
        agg_table = df[column].describe()[['min', '25%', '50%', '75%', 'max', 'mean']].to_frame()

    return agg_table


def get_countplot_imgdata(df, column, groupby=None):
    fig, ax = plt.subplots(figsize=(5, 4))
    custom_color = sns.color_palette('rocket', 3)
    sns.set_palette(custom_color)
    if groupby:
        sns.countplot(x=column, hue='difficulty', data=df, ax=ax)
        plt.legend(loc='upper right')
    else:
        sns.countplot(x=column, data=df, color='purple', ax=ax)
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    plt.close()

    return imgdata


def get_histogram_imgdata(df, column, groupby=None):
    fig, ax = plt.subplots(figsize=(5, 4))
    custom_color = sns.color_palette('rocket', 3)
    sns.set_palette(custom_color)
    if groupby:
        sns.violinplot(y=groupby, x=column, data=df, ax=ax)
    else:
        sns.histplot(df[column], color='purple', ax=ax)
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    plt.close()

    return imgdata


def get_piechart_imgdata(df_instance):
    plt.rc('font', family='Malgun Gothic')  # Korean Font for Windows
    plt.rc('font', family='AppleGothic')  # Korean Font for MAC
    fig = plt.figure(figsize=(5, 4))
    custom_color = sns.color_palette('rocket', 3)
    sns.set_palette(custom_color)
    ax = fig.add_subplot()
    ax.pie(labels=df_instance.index, 
            x=df_instance['Count'].values,
            startangle=0,
            autopct=lambda p : '{:.2f}%'.format(p))
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    plt.close()

    return imgdata
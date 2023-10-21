# -*- coding: utf-8 -*-
"""
irc.py

This file is used to plot irc path

@author:
Kimariyb, Hsiun Ryan (kimariyb@163.com)

@address:
XiaMen University, School of electronic science and engineering

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@data:
2023-10-16
"""
import proplot as pplt
import pandas as pd
import os 

from proplot import rc

def convert_energy(data: pd.DataFrame) -> pd.DataFrame:
    """将 DataFrame 第二列的数据单位从 Hartree 转化为 kcal/mol

    Args:
        data (pd.DataFrame): 一个 DataFrame 对象

    Returns:
        pd.DataFrame: 转换后的 DataFrame 对象
    """
    # 获取第二列的数据
    energy_column = data.iloc[:, 1]

    # 计算参考能量（以 Hartree 为单位）
    reference_energy = energy_column.min()

    # 将能量转换为相对能量（以 Hartree 为单位）
    relative_energy_hartree = energy_column - reference_energy

    # 将相对能量转换为kcal/mol（1 Hartree = 627.5095 kcal/mol）
    kcal_per_mol_conversion = 627.5095
    relative_energy_kcal = relative_energy_hartree * kcal_per_mol_conversion

    # 更新 DataFrame 的第二列数据
    data.iloc[:, 1] = relative_energy_kcal

    return data

if __name__ == "__main__":
    # 读取当前文件夹下的所有文件
    current_dir = os.getcwd()
    files_list = os.listdir(current_dir)
    # 过滤其他文件，只获取 txt 文件
    txt_files = [file for file in files_list if file.endswith('.txt')]

    # 读取 txt 文件中的 irc 数据，并将其保存在一个 irc_data 的 list 中
    irc_data = []
    for irc_file in txt_files:
        irc = pd.read_csv(irc_file, skiprows=4, header=None, delim_whitespace=True)
        # 将 irc 中的能量转化为 kcal/mol
        irc = convert_energy(irc)
        irc_data.append(irc)

    # 颜色列表，请注意索引
    color_list = ['#FA7F6F', '#82B0D2'] 

    # 设置绘图的默认参数，如字体、字号等
    rc['font.name'] = 'Arial'
    rc['title.size'] = 14
    rc['label.size'] = 12
    rc['font.size'] = 10.5
    rc['tick.width'] = 1.3
    rc['meta.width'] = 1.3
    rc['label.weight'] = 'bold'
    rc['tick.labelweight'] = 'bold'
    rc['ytick.major.size'] = 4.6
    rc['ytick.minor.size'] = 2.5
    rc['xtick.major.size'] = 4.6
    rc['xtick.minor.size'] = 2.5

    # 创建一个画布
    fig = pplt.figure(figsize=(5, 4.5), span=True, space=True)
    axs = fig.subplots(nrows=2, ncols=1)

    # 绘制多子图
    for ax, data, color in zip(axs, irc_data, color_list):
        x = data.iloc[:, 0]
        y = data.iloc[:, 1]
        # 绘制曲线
        ax.plot(x, y, linewidth=1.3, color=color)
        # 绘制实际的点
        ax.scatter(x, y, color=color, zorder=2, s=12)
        
        # 设置子图的 x-axis
        ax.format(
            xlim=(-10, 10), xminorlocator=1, xlocator=2, 
        )
       
    # 分别格式化每个子图的 y-axis
    axs[0].format(
        ylim=(0, 60), yminorlocator=5, ylocator=10
    ) 
    
    axs[1].format(
        ylim=(0, 60), yminorlocator=5, ylocator=10
    ) 

    # 格式化整个 axes
    axs.format(grid=False, abc='(a)', abcloc="ul")

    # 格式化 figure
    fig.format(
        suptitle='Total Energy along IRC',
        xlabel='Intrinsic Reaction Coordinate',
        ylabel='Total Energy (kcal/mol)'
    )

    # 保存图片
    fig.savefig('irc.png', bbox_inches='tight', dpi=300, pad_inches=0.2)

    print('successfully generated figure!')
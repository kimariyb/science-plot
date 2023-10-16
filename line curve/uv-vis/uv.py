# -*- coding: utf-8 -*-
"""
uv.py

This file is used to plot spectrum of uv-vis.

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

from proplot import rc

# 读取 txt 文件中的数据
data = pd.read_csv('uv_curve.txt', header=None, delim_whitespace=True)

# 颜色、曲线格式以及标签
color_list = ['black', 'red', 'orange', 'blue', 'green']
label_list = ['label1', 'label2', 'label3', 'label4', 'label5']
style_list = ['-', '--', '--', '--', '--']

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

# 创建画布
fig, ax = pplt.subplots(figsize=(6 * 0.9, 4 * 0.9))

# 绘制多曲线图
x = data.iloc[:, 0]
for i in range(len(data.columns) - 1):
    y = data.iloc[:, i + 1]
    ax.plot(x, y, linewidth=1.3, color=color_list[i], 
            label=label_list[i], linestyle=style_list[i])

# 设置图例
ax.legend(loc='ur', ncols=1, fontweight='bold', frame=False)

# 格式化图像
fig.format(
    grid=False, ylabel='Absorbance', xlabel='Wavelength (nm)',
    xlim=(80, 200), xminorlocator=10, xlocator=20, 
    ylim=(0, 10000), yminorlocator=1000, ylocator=2000
)

fig.show()

fig.savefig('uv.png', bbox_inches='tight', dpi=300)
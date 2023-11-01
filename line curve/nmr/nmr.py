# -*- coding: utf-8 -*-
"""
nmr.py

This file is used to plot NMR spectrum

@author:
Kimariyb, Hsiun Ryan (kimariyb@163.com)

@address:
XiaMen University, School of electronic science and engineering

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@data:
2023-11-01
"""

import proplot as pplt
import pandas as pd

from proplot import rc

if __name__ == "__main__":
    
    # 读取 1.csv 中的内容
    nmr_data = pd.read_csv('1.csv', header=None, delim_whitespace=True)
    
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
    fig = pplt.figure(figsize=(7 * 0.9, 4.5 * 0.9))
    ax = fig.subplots()
    
    ax.plot(nmr_data.iloc[:, 0], nmr_data.iloc[:, 1], color='#000000', linewidth=1)

    # 格式化图像
    fig.format(
        grid=False, ylabel='Absorbance', xlabel='Chemical Shift (ppm)',
        xlim=(10, 0), xminorlocator=0.5, xlocator=1, 
        ylim=(0, 0.14), yminorlocator=0.01, ylocator=0.02
    )
    
    fig.savefig('nmr.png', bbox_inches='tight', dpi=300)
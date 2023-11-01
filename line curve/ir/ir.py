# -*- coding: utf-8 -*-
"""
ir.py

This file is used to plot ir spectrum

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
    
    # 读取 ir.txt 中的内容
    ir_data = pd.read_csv('ir.txt', header=None, delim_whitespace=True)
    
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
    fig = pplt.figure(figsize=(6.7 * 0.9, 4.5 * 0.9))
    ax = fig.subplots()
    
    # 绘制曲线
    ax.plot(ir_data.iloc[:, 0], ir_data.iloc[:, 1], linewidth=1, color='#000000')

    # 格式化图像
    fig.format(
        grid=False, ylabel='Absorbance', xlabel='Wavenumber (cm^-1)',
        xlim=(4000, 0), xminorlocator=200, xlocator=400, 
        ylim=(1200, -200), yminorlocator=100, ylocator=200
    )
    
    fig.savefig('ir.png', bbox_inches='tight', dpi=300)
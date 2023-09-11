import numpy as np
import proplot as pplt

from proplot import rc


# 全局字体
fontname = "Arial"
# 全局字号，分别为普通字体、标签字体和标题字体
fontsize = [10.5, 12, 14]

# 设置绘图的默认参数，如字体、字号等
rc['font.family'] = fontname
rc['title.size'] = fontsize[2]
rc['label.size'] = fontsize[1]
rc['font.size'] = fontsize[0]
# 设置其他参数
rc['tick.width'] = 1.3
rc['meta.width'] = 1.3
rc['title.weight'] = 'bold'
rc['label.weight'] = 'bold'
rc['tick.labelweight'] = 'bold'
rc['ytick.major.size'] = 4.6
rc['ytick.minor.size'] = 2.5
rc['xtick.major.size'] = 4.6
rc['xtick.minor.size'] = 2.5

fig, ax = pplt.subplots(figsize=(5, 2))




fig.show()
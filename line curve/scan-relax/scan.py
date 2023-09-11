import numpy as np
import pandas as pd
import proplot as pplt

from proplot import rc
from scipy import interpolate


# 标题、x 和 y 轴 label
# 可以直接在 txt 中读取，也可以自行配置
title = None
xlabel = "Scan Coordinate"
ylabel = "Relative Energy (kJ/mol)"
# 如果 title、xlabel 和 ylabel 为 None 则在 txt 文件中找
# 打开 txt 文件，扫描 txt 文件中的前三行
with open('scan.txt', 'r', encoding='utf-8') as file:
    # 初始化 lines 变量
    lines = []
    for _ in range(3):
        line = file.readline().strip()
        # 判断是否存在 # 号开头的行
        if line.startswith('#'):
            line = line.lstrip('#').strip()
        # 如果不存在则直接跳出循环
        else:
            break
        lines.append(line)
    if title is None:
        title = lines[0]
    if xlabel is None:
        xlabel = lines[1]
    if ylabel is None:
        ylabel = lines[2]

# 全局字体
fontname = "Arial"
# 全局字号，分别为普通字体、标签字体和标题字体
fontsize = [10.5, 12, 14]
# 颜色主题，可以修改自己喜欢的颜色或者 16 进制颜色，第一个颜色为折线颜色，第二个颜色为点的颜色
colors = ["#D8005E", "#3233A6"]
# x 轴和 y 轴的刻度以及间距 [min, max, ticked]
xlim = [-180, 180, 60]
ylim = [-10, 40, 10]

# 使用 Pandas 读取 Gaussian 生成的 txt 文件中的数据
data = pd.read_csv("scan.txt", delim_whitespace=True, header=None, skiprows=4, names=['X', 'Y'])
# 将 DataFrame 对象中 Y 减去最小值 yMin 同时乘以 2625.51
data['Y'] = (data['Y'] - data['Y'].min()) * 2625.51

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

# 创建实例
fig, ax = pplt.subplots(figsize=(5.4 * 0.9, 4 * 0.9))

# 使用插值函数，让折线图变平滑
f = interpolate.interp1d(data['X'].values, data['Y'].values, kind='quadratic')
xNew = np.linspace(data['X'].min(), data['X'].max(), 101)
yNew = f(xNew)

# 绘制平滑曲线图
ax.plot(xNew, yNew, color=colors[0], linewidth=1.3, zorder=1)
# 绘制实际的点
ax.scatter(data['X'], data['Y'], color=colors[1], zorder=2, edgecolor='black')

# 格式化图像
fig.format(
    grid=False, ylabel=ylabel, xlabel=xlabel, title=title,
    xlim=(xlim[0], xlim[1]), xminorlocator=(xlim[2] / 2), xlocator=xlim[2], ylim=(ylim[0], ylim[1]),
    yminorlocator=(ylim[2] / 2), ylocator=ylim[2]
)

# 显示图像
fig.show()

# 保存图像
fig.savefig("scan.png", dpi=400, bbox_inches="tight")

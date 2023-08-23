import pandas as pd
import proplot as pplt
import matplotlib.pyplot

from proplot import rc

# 读取 Multiwfn 生成的 NICS-1D-all、sigma、pi 的数据
nics_pi = pd.read_csv("NICS_1D_pi.txt", delimiter="\s+")
nics_sigma = pd.read_csv("NICS_1D_sigma.txt", delimiter="\s+")
nics_all = pd.read_csv("NICS_1D_all.txt", delimiter="\s+")

# 设置绘图的默认参数，如字体、字号等
rc['font.family'] = "Arial"
rc['tick.width'] = 1.3
rc['meta.width'] = 1.3
rc['font.size'] = 9.5
rc['label.size'] = 12.5
rc['label.weight'] = 'bold'
rc['tick.labelweight'] = 'bold'
rc['ytick.major.size'] = 4.6
rc['ytick.minor.size'] = 2.5
rc['xtick.major.size'] = 4.6
rc['xtick.minor.size'] = 2.5

# 创建实例
fig, ax = pplt.subplots(figsize=(5.4 * 0.9, 4 * 0.9), dpi=300)
# 颜色 list
colors = ['off yellow', 'cherry red', 'true blue']

# 绘制整体贡献的 NICS 曲线
ax.plot(nics_all.iloc[:, -2], nics_all.iloc[:, -1], label='total', linewidth=1.2, color=colors[0])
# 绘制 sigma 体系贡献的 NICS 曲线
ax.plot(nics_sigma.iloc[:, -2], nics_sigma.iloc[:, -1], label='sigma', linewidth=1.2, color=colors[1])
# 绘制 pi 体系贡献的 NICS 曲线
ax.plot(nics_pi.iloc[:, -2], nics_pi.iloc[:, -1], label='pi', linewidth=1.2, color=colors[2])

# 在 y=0 处绘制一条虚线
axhline = ax.axhline(y=0, color='black', linewidth=1.2)
# 设置为最底层
axhline.set_zorder(0)

# 设置图例
ax.legend(loc='best', ncols=1, fontweight='bold', fontsize='12.5', frame=False, bbox_to_anchor=(0.95, 0.96))

# 格式化图像
fig.format(
    grid=False, ylabel='Shielding (in ppm)', xlabel='Position (in Å)',
    xlim=(-10, 10), xminorlocator=1, xlocator=2, ylim=(-30, 40), yminorlocator=5, ylocator=10
)

# 保存图像
fig.savefig("NICS.png", dpi=400, bbox_inches="tight")

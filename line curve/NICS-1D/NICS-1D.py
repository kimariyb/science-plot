import pandas as pd
import proplot as pplt

from proplot import rc

# 用于初始化变量
# 全局字体
fontname = "Arial"
# 全局字号，分别为普通字体、标签字体和标题字体
fontsize = [10.5, 12, 14]
# 颜色主题，可以修改自己喜欢的颜色或者 16 进制颜色
colors = ['red', 'blue', 'green']
# 判断 colors 是否为 None 或者空集合，如果为空集合或者 NONE，则使用默认的颜色集合
if colors is None or colors == []:
    # 默认为彩虹色
    # 红 #FF0000
    # 橙 #FF7F00
    # 黄 #FFFF00
    # 绿 #00FF00
    # 青 #00FFFF
    # 蓝 #0000FF
    # 紫 #8B00FF
    colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#8B00FF']

# 读取 Multiwfn 生成的 NICS-1D-all、sigma、pi 的数据
# 如果需要修改，请修改 NICS_1D_pi.txt、NICS_1D_sigma.txt 以及 NICS_1D_all.txt
nics_pi = pd.read_csv("NICS_1D_pi.txt", delim_whitespace=True, header=None)
nics_sigma = pd.read_csv("NICS_1D_sigma.txt", delim_whitespace=True, header=None)
nics_all = pd.read_csv("NICS_1D_all.txt", delim_whitespace=True, header=None)

# 设置绘图的默认参数，如字体、字号等
rc['font.family'] = fontname
rc['title.size'] = fontsize[2]
rc['label.size'] = fontsize[1]
rc['font.size'] = fontsize[0]
# 设置其他参数
rc['tick.width'] = 1.3
rc['meta.width'] = 1.3
rc['label.weight'] = 'bold'
rc['tick.labelweight'] = 'bold'
rc['ytick.major.size'] = 4.6
rc['ytick.minor.size'] = 2.5
rc['xtick.major.size'] = 4.6
rc['xtick.minor.size'] = 2.5

# 创建实例
fig, ax = pplt.subplots(figsize=(5.4 * 0.9, 4 * 0.9))

# 绘制整体贡献的 NICS 曲线
ax.plot(nics_all.iloc[:, -2], nics_all.iloc[:, -1], label='total', linewidth=1.2, color=colors[0])
# 绘制 sigma 体系贡献的 NICS 曲线
ax.plot(nics_sigma.iloc[:, -2], nics_sigma.iloc[:, -1], label='sigma', linewidth=1.2, color=colors[1])
# 绘制 pi 体系贡献的 NICS 曲线
ax.plot(nics_pi.iloc[:, -2], nics_pi.iloc[:, -1], label='pi', linewidth=1.2, color=colors[2])

# 在 y=0 处绘制一条虚线
ax_line = ax.axhline(y=0, color='black', linewidth=1.2)
# 设置为最底层
ax_line.set_zorder(0)

# 设置图例
ax.legend(loc='ur', ncols=1, fontweight='bold', fontsize='12.5', frame=False, bbox_to_anchor=(0.95, 0.96))

# 格式化图像
fig.format(
    grid=False, ylabel='Shielding (in ppm)', xlabel='Position (in Å)',
    xlim=(-10, 10), xminorlocator=1, xlocator=2, ylim=(-30, 40), yminorlocator=5, ylocator=10
)

# 显示图像
fig.show()

# 保存图像
fig.savefig("NICS.png", dpi=400, bbox_inches="tight")

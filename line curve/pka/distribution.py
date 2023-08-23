import numpy as np
import proplot as pplt

from proplot import rc

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

# 创建一个 list 用来保存 Acid 或 Base 的 Ka 或 Kb
# 例如二元酸草酸的 Ka1 和 Ka2 保存为 ka_list，可以自行添加或删改
ka_list = [5.9e-2, 6.4e-5]

# x 和 y 轴数据
x = np.linspace(0, 14, 10 * 14 + 1)
y = np.ones((2, 10 * 14 + 1), dtype=np.float64)
# H 离子
proton = np.power(10, -x)

for i in np.arange(2):
    for k in 1 + np.arange(i): y[i] *= ka_list[k]
    y[i] *= proton ** (2 - i)

s = sum(y)
y /= s

# 创建实例
fig, ax = pplt.subplots(figsize=(5.4 * 0.9, 4 * 0.9), dpi=300)

for i in range(2):
    ax.plot(x, y[i])

# 设置图例
ax.legend(loc='best', ncols=1, fontweight='bold', fontsize='12.5', frame=False, bbox_to_anchor=(0.95, 0.96))

# 格式化图像
fig.format(
    grid=False, ylabel='Fraction', xlabel='pH',
    xlim=(0, 14), xminorlocator=1, xlocator=2, ylim=(0, 1), yminorlocator=0.1, ylocator=0.2
)

# 显示图像
fig.show()

# 保存图像
# fig.savefig("NICS.png", dpi=400, bbox_inches="tight")

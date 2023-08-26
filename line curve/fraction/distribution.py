import numpy as np
import proplot as pplt
import toml

from proplot import rc

# 设置绘图的默认参数，如字体、字号等
rc['font.name'] = "Arial"
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


def calculate_deltas(pH, n, K):
    """
    计算 n 元弱酸的分布分数 delta
    :param pH: 体系的 pH 值
    :param n: n 元弱酸
    :param K: 解离平衡常数 K
    :return: 返回分布分数 delta
    """
    # 将 pH 转换为氢离子浓度 C
    C = 10 ** (-pH)

    # 首先计算 S(n)，因为所有的分布分数的结果
    S = np.sum([(C ** ((n + 1) - i)) * np.prod(K[:i - 1]) for i in range(1, n + 1)])

    # 计算 F(n, i)
    F = np.zeros(n + 1)
    for i in range(n + 1):
        F[i] = (C ** (n - i)) * np.prod(K[:i])

    # 计算归一化的分布分数
    distributions = F / S

    return distributions


def plot_distribution_curve(n, K):
    """
    绘制分布分数-pH曲线图
    :param n: n 元弱酸
    :param K: 解离平衡常数 K
    """
    # 设置需要绘制的 pH 的范围为 0 ~ 14
    pH_range = np.linspace(0, 14, 500)
    # 初始化 distributions
    distributions = np.zeros((n + 1, len(pH_range)))

    # 计算每个 pH 值对应的分布分数
    for i, pH in enumerate(pH_range):
        distributions[:, i] = calculate_deltas(pH, n, K)

    # 归一化分布分数
    sum_distribution = np.sum(distributions, axis=0)
    normalized_distributions = distributions / sum_distribution

    # 创建实例
    fig, ax = pplt.subplots(figsize=(5.4 * 0.9, 4 * 0.9), dpi=300)

    # 如果想设置其他颜色循环可以使用 cycle 参数
    # for i in range(n + 1):
    #     ax.plot(pH_range, normalized_distributions[i, :], label=f'δ{n}({i + 1})', cycle='bmh')
    # 或者直接用 pplt.rc.cycle = '538' 调整 cycle 参数
    # 如果想使用自定义颜色可以使用 color 参数
    # color_list = ['填你想要的颜色']
    # for i in range(n + 1):
    #     ax.plot(pH_range, normalized_distributions[i, :], label=f'δ{n}({i + 1})', color=color_list[i])

    # 绘制分布曲线
    for i in range(n + 1):
        ax.plot(pH_range, normalized_distributions[i, :], label=f'δ{n}({i + 1})', linewidth=1.3)

    # 设置图例
    ax.legend(loc='ur', ncols=1, fontweight='bold', fontsize='12.5', frame=True)

    # 格式化图像
    fig.format(
        grid=False, ylabel='Fraction', xlabel='pH Values',
        xlim=(0, 14), xminorlocator=1, xlocator=2, ylim=(0, 1), yminorlocator=0.1, ylocator=0.2
    )

    # 显示图像
    fig.show()

    return fig, ax


# 读取 equilibrium.toml 中的数据
equilibrium = toml.load("equilibrium.toml")
# 将每一个 K 的 value 记录到一个  list K_values 中
K_values = [item['value'] for item in equilibrium.get("K")]

# 根据 K_values list 拿到 n
acid_num = len(K_values)
# 绘制图像
fig, ax = plot_distribution_curve(acid_num, K_values)

# 保存图像
fig.savefig("delta.png", dpi=400, bbox_inches="tight")

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


def sum_function(k_list, pH):
    """
    该方法实现了通过 K、pH 求解化学平衡分布分数 delta 的具体值
    :param k_list: 由解离平衡常数组成的 list
    :param pH: pH 值
    :return: 根据 pH 和 K_list 得到 delta
    """
    # 初始化求和系数 S(x)
    F_sum = 0
    # 首先得到所有解离平衡常数 list 的长度 k_num，根据 k_num 推断所需要计算的 delta 存在几元解离平衡
    k_num = len(k_list)
    # 外部循环，对应最外的累加符号，也就是从 i=0 开始到 i=x 累加，x 为 1，2，3...等正整数，实际上等于 x = k_num + 1
    for i in range(0, k_num + 1):
        # 初始化 K 项
        K_item = 1
        # 计算 C^{x-i} 项的值 C_item
        C_item = pH ** (k_num + 1 - i)
        # 内部循环，对应内部的累乘符号，也就是从 j=1 开始到 j=i 累乘，如果 i=0 就省去这一项
        for j in range(1, i):
            # 计算 prod{K_j} 项的值 K_item
            K_item *= k_list[j - 1]
        # 将每一项都累加起来得到最终的 S(x)
        F_sum += C_item * K_item

    return F_sum


# 读取 equilibrium.toml 中的数据
equilibrium = toml.load("equilibrium.toml")
# 将每一个 K 的 value 记录到一个  list K_values 中
K_values = [item['value'] for item in equilibrium.get("K")]

# 设置 pH 的范围
ph_values = np.linspace(0, 14, 100)

# 新建一个 numpy 数组用来存放不同 pH 下的数据
sum_list = np.array([])
# 根据 pH 得到 delta 的分母
for ph_value in ph_values:
    sum_list = np.append(sum_list, sum_function(k_list=K_values, pH=ph_value))

# 计算每一个组分的分布分数。如果是一个二元弱酸，则有 3 种组分，三个分布分数 delta，
# 需要使用一个 [[nparray1],[nparray2],[nparray3]] 集合保存，以此类推
# 初始化一个空集合 delta_list 用来存放不同 delta 对应的 values
delta_list = []
# 循环 pH 数据以及 sum 数据
for ph_value, sum_value in zip(ph_values, sum_list):
    # 用于存放同一个 i 中的所有 delta
    delta_i = np.array([])
    for i in range(0, len(K_values) + 1):
        # 初始化 product
        product = 1
        for j in range(1, i):
            product *= K_values[j - 1]
        # 分子除以分母得到 delta
        F_x = ph_value ** (len(K_values) + 1 - i) * product
        delta = F_x / sum_value
        # 将同一个 i 中的所有 delta 存放在一个 numpy array 中
        delta_i = np.append(delta_i, delta)

    print(delta_i)

"""
# 计算分布分数 delta 值
delta_values = None

# 创建实例
fig, ax = pplt.subplots(figsize=(5.4 * 0.9, 4 * 0.9), dpi=300)

# 绘制每一个组分下对应的曲线
for delta_value in delta_values:
    ax.plot(ph_values, delta_value)

# 设置图例
ax.legend(loc='best', ncols=1, fontweight='bold', fontsize='12.5', frame=False, bbox_to_anchor=(0.95, 0.96))

# 格式化图像
fig.format(
    grid=False, ylabel='Fraction', xlabel='pH Values',
    xlim=(0, 14), xminorlocator=1, xlocator=2, ylim=(0, 1), yminorlocator=0.1, ylocator=0.2
)

# 显示图像
fig.show()

# 保存图像
# fig.savefig("NICS.png", dpi=400, bbox_inches="tight")
"""

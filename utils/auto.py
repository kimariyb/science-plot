import math


def auto_lim(max_value, min_value, is_deviation=False):
    """
    根据最大值和最小值，自动生成一个较为整齐的 xlim 或 ylim，lim 包括 x 或 y 轴的最大值，x 或 y 轴的最小值，
    以及 x 或 y 轴的刻度 locator
    :param max_value: x 或 y 数据的最大值
    :param min_value: x 或 y 数据的最小值
    :param is_deviation 是否允许误差，默认为 False
    :return: 返回一个 auto lim list [lim_min, lim_max, locator]
    """
    # 初始化一个理想的刻度间隔段数，即希望刻度区间有多少段
    split_number = 4
    # 初始化一个魔术数组
    magic_array = [2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]  # 计算出初始间隔 temp_gap 和缩放比例 multiple
    temp_gap = (max_value - min_value) / split_number
    # temp_gap 除以 magic_array 后刚刚处于魔数区间内，先求 multiple 的幂 10 指数，
    # 例如当 temp_gap 为 120，想要把 temp_gap 映射到魔数数组（即处理为 10 到 100 之间的数），则倍数为 10，即 10 的 1 次方。
    multiple = 10 ** (math.floor(math.log10(temp_gap) - 1))
    # 查找大于temp_gap / multiple的第一个魔术数字
    estep = next((val * multiple for val in magic_array if val > temp_gap / multiple), None)

    # 求出期望的最大刻度和最小刻度，为 estep 的整数倍
    maxi, mini = count_degree(estep, max_value, min_value)

    if not is_deviation:
        while True:
            temp_split_number = round((maxi - mini) / estep)
            # 根据条件判断更新最大值和最小值
            if (maxi == 0 or mini - min_value <= maxi - max_value) and temp_split_number < split_number:
                mini -= estep  # 更新最小值（向左移动）
            else:
                maxi += estep  # 更新最大值（向右移动）
            # 达到预期的分割数量，退出循环
            if temp_split_number == split_number:
                break
            if temp_split_number > split_number:
                # 查找当前魔术数字的索引
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == estep), None)
                # 如果索引存在且不是最后一个，更新 estep 和最大值最小值
                if magic_idx is not None and magic_idx < len(magic_array) - 1:
                    estep = magic_array[magic_idx + 1] * multiple  # 更新 estep（增加）
                    maxi, mini = count_degree(estep, max_value, min_value)  # 更新最大值和最小值
                else:
                    break
            else:
                # 查找当前魔术数字的索引
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == estep), None)
                # 如果索引存在且不是第一个，更新 estep 和最大值最小值
                if magic_idx is not None and magic_idx > 0:
                    estep = magic_array[magic_idx - 1] * multiple  # 更新 estep（减少）
                    maxi, mini = count_degree(estep, max_value, min_value)  # 更新最大值和最小值
                else:
                    break

    # 得到间距
    interval = (maxi - mini) / split_number

    lim = [mini, maxi, interval]

    return lim


def count_degree(estep, max_value, min_value, symmetrical=False):
    """
    求出期望的最大刻度和最小刻度，为 estep 的整数倍
    :param estep: 最佳期望的间隔
    :param max_value: 数据的最大值
    :param min_value: 数据的最小值
    :param symmetrical: 是否开启正负刻度
    :return:
    """
    # 最终效果是当 max/estep 属于 (-1,Infinity) 区间时，向上取 1 格，否则取 2 格。
    # 当 min/estep 属于 (-Infinity,1) 区间时，向下取 1 格，否则取 2 格。
    maxi = int(max_value / estep + 1) * estep
    mini = int(min_value / estep - 1) * estep
    # 如果 max 和 min 刚好在刻度线的话，则按照上面的逻辑会向上或向下多取一格
    if max_value == 0:
        maxi = 0
    if min_value == 0:
        mini = 0
    if symmetrical and maxi * mini <= 0:
        tm = max(abs(maxi), abs(mini))
        maxi = tm
        mini = -tm

    return maxi, mini

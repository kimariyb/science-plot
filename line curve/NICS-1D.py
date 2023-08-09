import pandas as pd
import seaborn as sns

# 读取 Multiwfn 生成的 NICS-1D-all、sigma、pi 的数据
nics_pi = pd.read_csv("./NICS-1D/NICS_1D_pi.txt", delimiter="\s+")
nics_sigma = pd.read_csv("./NICS-1D/NICS_1D_sigma.txt", delimiter="\s+")
nics_all = pd.read_csv("./NICS-1D/NICS_1D_all.txt", delimiter="\s+")



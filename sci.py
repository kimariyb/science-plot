import numpy as np
import matplotlib.pyplot as plt
import scienceplots

def model(x, p):
    return x ** (2 * p + 1) / (1 + x ** (2 * p))

pparam = dict(xlabel='Voltage (mV)', ylabel='Current ($\mu$A)')

x = np.linspace(0.75, 1.25, 201)

with plt.style.context(['science', 'nature']):
    fig, ax = plt.subplots()
    for p in [10, 15, 20, 30, 50, 100]:
        ax.plot(x, model(x, p), label=p)
    ax.legend(title='Order')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    fig.savefig('./fig1.jpg', dpi=500)
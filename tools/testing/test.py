# testing packages and calcs


import utils.units.units as uu
from utils.stdatmos import stdatmos
import design.wing.wing as wing
import design.weights.weights as wt
import matplotlib.pyplot as plt


wing = wing.wing()
print(wing.planform(714.3, 8, .35, 31.5))
print(wing.drag(0.82, 36000, 0.12, 0.4, 0.3171, 0.8, -1.33))
# plt.show()

itertow = wt.weights()
itertows = itertow.itertow(.82, 3800, 36000, 2600, 0.65, 8, 0.6, 45, 5, 1)
print(itertows)

WSs = wing.wingload(itertows)
print(WSs)
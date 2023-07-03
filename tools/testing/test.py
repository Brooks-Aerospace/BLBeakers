# testing packages and calcs

import utils.units as uu
from utils.stdatmos import stdatmos
import design.wing as wing
import design.weights as wt
import design.fuse as fuse
import matplotlib.pyplot as plt
import numpy as np


# create and test wing planform and drag
wing = wing.wing()
plt.figure()
wing.planform(714.3, 8, .35, 31.5)
# print(wing.planform(714.3, 8, .35, 31.5))
# cruiseCL = wing.cruiseCL(5, 0.8)
# print(wing.drag(0.82, 36000, 0.12, 0.4, cruiseCL, -1.33))
# plt.show()

# test itertow
itertow = wt.weights()
itertows = itertow.itertow(.82, 3800, 36000, 2600, 0.65, 8, 0.6, 45, 5, 1)
# print(itertows)

# test wingload
WSs = wing.wingload(itertows)
# print(WSs[0])

# test groundroll
ToL = np.array(wing.groundroll(WSs[0], 0.3548, [1.89, 2.1], 0))
# print(ToL)

# test psc gen
fuse = fuse.fuse()
plt.figure()
fuse.PSCylGen(7, 11.5, [0.4, 0.2], 0.6)
plt.show()
# Simple Aircraft Fuselage Generator
# Slade Brooks
# spbrooks4@gmail.com

import numpy as np
import matplotlib.pyplot as plt
from utils.stdatmos import stdatmos


class fuse():
    """
    This class contains a simple generator for an aircraft fuselage.
    
    Methods
    -------
    PSCylGen(D, fr, Lcs, n)
        Generates geometry and drag calcs for a power series cylinder fuse.
    PSCylDrag()
        Estimates the wetted area, drag, and CD0 of a power series cylinder fuse.
    """
    
    def PSCylGen(self, D, fr, Lcs, n):
        """
        This method creates a simple power series cylinder fuselage and returns a plot of it.
        
        Parameters
        ----------
        D : float
            Max diameter.
        fr : float
            Fineness ratio.
        Lcs : np.ndarray
            Numpy array of [nose, tail] intersection points as decimal percent of length.
        n : float
            Nose/tail "sharpness," decimal percent.
        """
# Simple Aircraft Fuselage Generator
# Slade Brooks
# spbrooks4@gmail.com

import numpy as np
import matplotlib.pyplot as plt
from utils.stdatmos import stdAtmos


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
            
        Returns
        -------
        L : float
            Fuselage length.
        xs : np.ndarray
            Numpy array of fuselage x stations.
        Ds : np.ndarray
            Numpy array of fuselage diameters at each x station.
        fr : float
            Fuselage fineness ratio.
        """
        
        # determine the length
        L = fr*D
        fr = fr
        
        # define set of x locations and corresponding actual locations
        xLs = np.arange(0, 1.001, 0.02)
        xs = xLs*L
        
        # determine diameter at each point
        Ds = np.zeros_like(xLs)
        for i, x in enumerate(xs):
            # if location is not along nose or tail
            if x > Lcs[0]*L and x < (1 - Lcs[1])*L:
                Ds[i] = D

            # if along nose
            elif x <= Lcs[0]*L:
                Ds[i] = D*((x/(Lcs[0]*L))**n)

            # if along tail
            elif x >= (1 - Lcs[1])*L:
                Ds[i] = D*(((L - x)/(Lcs[1]*L))**n)
                
        # create array of positive and negative ys for plotting
        ys = Ds/2
        ysn = -1*Ds/2

        # plot fuse shape
        plt.plot(xs, ys, "k-")
        plt.plot(xs, ysn, "k-")
        plt.gca().set_aspect("equal")
        plt.grid()
        plt.xlim((-1, xs[-1] + 1))
        plt.ylim((-D/2 - 1, D/2 + 1))
        plt.xlabel("Length (ft)")
        plt.ylabel("Height (ft)")
        
        # store fuse info
        self.L = L
        self.D = D
        self.fr = fr
        self.plot = np.array([xs, ys])
        self.xs = xs
        self.Ds = Ds
        
        return L, xs, Ds, fr, D


    def PSCylDrag(self, PSCyl, Mc, alt, S):
        """
        This method estimates the drag of a power series cylinder fuselage generated by PSCYlGen.
        
        Parameters
        ----------
        PSCyl : function
            Instance of PSCylGen method.
        Mc : float
            Cruise mach number.
        alt : float
            Cruise altitude.
        S : float
            Wing reference area (ft^2).
            
        Returns
        -------
        Swet : float
            Fuselage wetted area.
        Drag : float
            Fuselage total drag.
        """
        
        # get stuff from function
        L = PSCyl.L
        xs = PSCyl.xs
        Ds = PSCyl.Ds
        fr = PSCyl.fr
        D = PSCyl.D
        std = stdAtmos()
        q = std.qMs(alt)*(Mc**2)
        
        # determine perimeter @ each location
        Ps = Ds*np.pi
        
        # determine wetted area @ each location
        Swets = np.zeros(((len(xs) - 1), 1))
        for i in range(1, len(xs)):
            Swets[i - 1] = Ps[i]*(xs[i] - xs[i - 1])
        
        # sum for total Swet
        Swet = np.sum(Swets)
        
        # get Re
        Vc = std.Aspeed(alt)*Mc
        Res = np.zeros(((len(xs) - 1), 1))
        for k in range(1, len(xs)):
            Res[k - 1] = Vc*xs[k]/std.VRkin(alt)

        # get Cf
        Cfs = np.zeros_like(Res)
        for j, Re in enumerate(Res):
            if Re < 1000000:
                Cfs[j] = 1.328/np.sqrt(Re)
            else:
                Cfs[j] = 0.455/((np.log10(Re)**2.58)*(1 + 0.144*Mc**2)**0.65)

        # get drag along fuse
        ff = 1 + (60/fr**3) + fr/400
        Drags = Cfs*Swets*q*ff
        Drag = np.sum(Drags)
        
        # calc and add wave drag
        Amax = (np.pi*D**2)/4
        cdw = 4*Amax/(np.pi*(L/2)**2)
        dw = Amax*cdw*q
        Drag += dw
        
        return Swet, Drag
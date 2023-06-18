# Aircraft Wing Design Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet


import numpy as np
import matplotlib.pyplot as plt
import sys
import os
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd, "..\\..\\"))
import stdatmos.standardAtmosphere as atmos


class wing():
    """
    This class contains the equations to determine an aircraft wing planform.
    
    Methods
    -------
    planform(S, ar, taper, LEsweep)
    drag()
    """
        
    def planform(self, S, ar, taper, LEsweep):
        """
        This method determines the planform characteristics of a wing given its design parameters. It returns the values
        of these parameters as well as a plot of the wing plan view.
        
        Parameters
        ----------
        S : float
            Wing area.
        AR : float
            Aspect ratio.
        taper : float
            Taper ratio.
        LEsweep : float
            Leading edge sweep (deg).
        
        Returns
        -------
        b : float
            Span.
        cr : float
            Root chord.
        ct : float
            Tip chord.
        mac : float
            Mean aerodynamic chord.
        ymac : float
            Location of MAC on the wing.
        LEsweep : float
            Leading edge sweep angle.
        qcsweep : float
            Quarter chord sweep angle.
        TEsweep : float
            Trailing edge sweep angle.
        """
        
        # calculate span
        b = np.sqrt(S*ar)
        
        # calculate root and tip chord
        cr = 2*b/(ar*(1 + taper))
        ct = cr*taper
        
        # calculate MAC and location
        mac = 2*cr/3*(1 + taper + taper**2)/(1 + taper)
        ymac = b/6*(1 + 2*taper)/(1 + taper)
        
        # calculate sweep angles
        LEsweep = np.degrees(np.arctan(np.tan(np.radians(LEsweep)) - 0*(2*cr*(1 - taper)/b)))
        qcsweep = np.degrees(np.arctan(np.tan(np.radians(LEsweep)) - 0.25*(2*cr*(1 - taper)/b)))
        TEsweep = np.degrees(np.arctan(np.tan(np.radians(LEsweep)) - 1*(2*cr*(1 - taper)/b)))
        
        # plotting of planform
        xs = np.array([0, cr, cr + b/2*np.tan(np.radians(TEsweep)), b/2*np.tan(np.radians(LEsweep)), 0])
        ys = np.array([0, 0, b/2, b/2, 0])
        plt.plot(xs, ys, "k-")
        plt.xlim([-1, xs[2] + 1])
        plt.ylim([0, ys[2] + 1])
        plt.gca().set_aspect("equal")
        plt.grid()
        plt.xlabel("Chordwise Location (ft)")
        plt.ylabel("Spanwise Location (ft)")
        
        # save wing info
        self.S = S
        self.ar = ar
        self.taper = taper
        self.LEsweep = LEsweep
        self.b = b
        self.cr = cr
        self.ct = ct
        self.mac = mac
        self.ymac = ymac
        self.qcsweep = qcsweep
        self.TEsweep = TEsweep
        
        return b, cr, ct, mac, ymac, LEsweep, qcsweep, TEsweep
   
    def drag(self, Mc, alt, tc, tcmax, Cl, e, a0L):
        """
        This method determines the drag characteristics of the planform determined in the planform() method. It returns
        the 0 lift drag of the wing as well as the total drag of the wing during cruise.
        
        Parameters
        ----------
        alt : float
            Cruise altitude.
        e : float
            Wing efficiency factor.
        Mc : float
            Cruise Mach number.
        tc : float
            Wing t/c.
        tcmax : float
            Airfoil max thickness location.
        Cl : float
            Cruise Cl.
        a0L : float
            Airfoil zero lift aoa.
            
        Returns
        -------
        """
        
        std = atmos.standardAtmosphere()

        # get cruise speed and effective speed and Mach
        Vc = Mc*std.Aspeed(alt)[0]
        Veff = Vc*np.cos(np.radians(self.LEsweep))
        Meff = Mc*np.cos(np.radians(self.LEsweep))
        
        # Reynold's num
        Remac = Veff*self.mac/std.VRkin(alt)[0]
        
        # calculate Cf
        if Remac < 1000000:
            Cf = 1.328/np.sqrt(Remac)
        else:
            Cf = 0.455/((np.log10(Remac)**2.58)*(1 + 0.144*Meff**2)**0.65)

        # also get Swet
        if tc <= 0.05:
            Swet = 2.003*self.S
        else:
            Swet = (1.977 + 0.52*tc)*self.S
            
        # calculate F??
        tcsweep = np.degrees(np.arctan(np.tan(np.radians(self.LEsweep)) - tcmax*(2*self.cr*(1 - self.taper)/self.b)))
        F = (1 + 0.6/tcmax*tc + 100*tc**4)*(1.34*(Mc**0.18)*np.cos(np.radians(tcsweep))**0.28)
        
        # now get wing CD0
        Cd0 = Cf*Swet*F/self.S
        
        # get beta if beta can exist
        if Meff < 1:
            B = np.sqrt(1 - Meff**2)
            
        # calc Cla
        CLa = np.pi/180*2*np.pi*self.ar/(2 + np.sqrt(4 + self.ar**2*B**2*(1 + np.tan(np.radians(tcsweep))**2/B**2)))
        
        # get Clo
        CLo = -CLa*a0L
        
        # now get the trim CL
        atrim = (Cl - CLo)/CLa
        CLtrim = CLo + CLa*atrim
        
        # get K
        K = 1/(np.pi*self.ar*e)
        
        # get total CD and then total drag
        Cd = Cd0 + K*CLtrim**2
        drag = Cd*self.S*std.qMs(alt)[0]*Mc**2
        
        return drag, Cd0


if __name__ == "__main__":
    wing = wing()
    print(wing.planform(714.3, 8, .35, 31.5))
    print(wing.drag(0.82, 36000, 0.12, 0.4, 0.3171, 0.8, -1.33))
    # plt.show()
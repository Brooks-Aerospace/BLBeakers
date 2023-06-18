# Aircraft Wing Design Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet


import numpy as np
import matplotlib.pyplot as plt


class wing():
    """
    This class contains the equations to determine an aircraft wing planform.
    
    Methods
    -------
    """
    
    def __init__(self):
        """
        , M, S, AR, ALE, tc, taper, Wo, Wf, qo, qf, Cl, alt, e)
        Parameters
        ----------
        M : float
            Cruise Mach number.
        S : float
            Wing area.
        AR : float
            Wing aspect ratio.
        ALE : float
            Leading edge sweep angle.
        tc : float
            Wing thickness to chord ratio.
        taper : float
            Wing taper ratio.
        Wo : float
            Initial cruise weight.
        Wf : float
            Final cruise weight.
        qo : float
            Initial cruise dynamic pressure.
        qf : float
            Final cruise dynamic pressure.
        Cl : float
            Cruise CL.
        alt : float
            Cruise altitude.
        e : float
            Wing efficiency factor.
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
        plt.xlim([0, xs[2] + 1])
        plt.ylim([0, ys[2] + 1])
        plt.gca().set_aspect("equal")
        plt.grid()
        plt.xlabel("Chordwise Location (ft)")
        plt.ylabel("Spanwise Location (ft)")
        
        return b, cr, ct, mac, ymac, LEsweep, qcsweep, TEsweep
        
    def viscDrag():
        """
        
        """


if __name__ == "__main__":
    wing = wing()
    print(wing.planform(714.3, 8, 0.35, 31.5))
    plt.show()
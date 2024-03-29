# Aircraft Wing Design Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet

import numpy as np
import matplotlib.pyplot as plt
from utils.stdatmos import stdAtmos
# set up standard atmosphere
std = stdAtmos()


class wing():
    """
    This class contains the equations to determine an aircraft wing planform.
    
    Methods
    -------
    planform(S, ar, taper, LEsweep)
        Returns plot of wing planform, b, cr, ct, mac, ymac, LEsweep, qcsweep, and TEsweep.
    cruiseCL(Swetref, e)
        Determines the cruise CL.
    drag(Mc, alt, tc, tcmax, cruiseCl, a0L)
        Returns wing total drag and Cd0.
    wingload(itertow)
        Returns the wingloading and weights throughout flight.
    groundroll(wingload, twrT, CLmaxs, alt)
        Returns the takeoff and landing ground roll at a given altitude.
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
        self.plot = np.array([xs, ys])
        
        return b, cr, ct, mac, ymac, LEsweep, qcsweep, TEsweep
    

    def drag(self, Mc, alt, tc, tcmax, a0L, Swetref, e):
        """
        This method determines the drag characteristics of the planform determined in the planform() method. It returns
        the 0 lift drag coefficient of the wing as well as the total drag of the wing during cruise.
        
        Parameters
        ----------
        alt : float
            Cruise altitude.
        Mc : float
            Cruise Mach number.
        tc : float
            Wing t/c.
        tcmax : float
            Airfoil max thickness location.
        a0L : float
            Airfoil zero lift aoa.
        Swetref : float
            Swet/Sref of the aircraft.
        e : float
            Wing efficiency factor.
            
        Returns
        -------
        drag : float
            Total wing drag.
        Cd0 : float
            Wing zero lift drag coefficient.
        """
        # calculate Cd0
        cd0 = 0.003*Swetref
        
        # get K
        self.e = e
        self.K = 1/(np.pi*self.ar*e)
        
        # determine cruise CL
        cruiseCL = np.sqrt(cd0/(3*self.K))

        # get cruise speed and effective speed and Mach
        Vc = Mc*std.Aspeed(alt)
        Veff = Vc*np.cos(np.radians(self.LEsweep))
        Meff = Mc*np.cos(np.radians(self.LEsweep))
        
        # Reynold's num
        Remac = Veff*self.mac/std.VRkin(alt)
        
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
        else:
            raise Exception("Cruise speed is supersonic and idk what to do :(")
            
        # calc Cla
        CLa = np.pi/180*2*np.pi*self.ar/(2 + np.sqrt(4 + self.ar**2*B**2*(1 + np.tan(np.radians(tcsweep))**2/B**2)))
        
        # get Clo
        CLo = -CLa*a0L
        
        # now get the trim CL
        atrim = (cruiseCL - CLo)/CLa
        CLtrim = CLo + CLa*atrim
        
        # get total CD and then total drag
        Cd = Cd0 + self.K*CLtrim**2
        drag = Cd*self.S*std.qMs(alt)*Mc**2
        
        return drag, Cd0
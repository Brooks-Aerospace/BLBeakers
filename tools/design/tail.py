# Aircraft Tail Design Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet

import sys
sys.path.append("C:\\Users\\spbro\\Documents\\BLBeakers\\tools\\")
import numpy as np
import matplotlib.pyplot as plt
from utils.stdatmos import stdAtmos
# set up standard atmosphere
std = stdAtmos()
from design.wing import wing
from design.fuse import fuse


class vertTail():
    """
    This class contains the equations to determine an aircraft vertical tail planform.
   
    # TODO: fix documentation
    """
    def __init__(self, wing, fuse):
        self.wing = wing
        self.fuse = fuse
       
       
    def planform(self, C, IIf, taper, LEsweep, AR):
        """
        This method determines the planform characteristics of a wing given its design parameters. It returns the values
        of these parameters as well as a plot of the wing plan view.
       
        # TODO: fix docs
        """
        # calculate I
        I = IIf*self.fuse.L
       
        # calculate area
        S = C*self.wing.b*self.wing.S/I
       
        # calculate h
        h = np.sqrt(AR*S)
       
        # calculate root and tip chord
        cr = 2*h/(AR*(1 + taper))
        ct = cr*taper
       
        # calculate MAC and location
        mac = 2*cr/3*(1 + taper + taper**2)/(1 + taper)
        ymac = h/3*(1 + 2*taper)/(1 + taper)
       
        # calculate sweep angles
        LEsweep = np.degrees(np.arctan(np.tan(np.radians(LEsweep)) - 0*(cr*(1 - taper)/h)))
        qcsweep = np.degrees(np.arctan(np.tan(np.radians(LEsweep)) - 0.25*(cr*(1 - taper)/h)))
        TEsweep = np.degrees(np.arctan(np.tan(np.radians(LEsweep)) - 1*(cr*(1 - taper)/h)))
       
        # plotting of planform
        xs = np.array([0, cr, cr + h*np.tan(np.radians(TEsweep)), h*np.tan(np.radians(LEsweep)), 0])
        ys = np.array([0, 0, h, h, 0])
        plt.plot(xs, ys, "k-")
        plt.xlim([-1, xs[2] + 1])
        plt.ylim([0, ys[2] + 1])
        plt.gca().set_aspect("equal")
        plt.grid()
        plt.xlabel("Chordwise Location (ft)")
        plt.ylabel("Spanwise Location (ft)")
       
        # save vert tail info
        self.S = S
        self.AR = AR
        self.taper = taper
        self.LEsweep = LEsweep
        self.h = h
        self.cr = cr
        self.ct = ct
        self.mac = mac
        self.ymac = ymac
        self.qcsweep = qcsweep
        self.TEsweep = TEsweep
        self.plot = np.array([xs, ys])
       
        return h, cr, ct, mac, ymac, LEsweep, qcsweep, TEsweep
   
   
    def drag(self, Mc, alt, tc, tcmax):
        """
        This method determines the drag characteristics of the planform determined in the planform() method. It returns
        the 0 lift drag coefficient of the tail as well as the total drag of the tail during cruise.
       
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
        tcsweep = np.degrees(np.arctan(np.tan(np.radians(self.LEsweep)) - tcmax*(self.cr*(1 - self.taper)/self.h)))
        F = 1.1*(1 + 0.6/tcmax*tc + 100*tc**4)*(1.34*(Mc**0.18)*np.cos(np.radians(tcsweep))**0.28)
       
        # now get wing CD0 adn drag
        Cd0 = 1.05*Cf*Swet*F/self.wing.S
        drag = Cd0*self.S*std.qMs(alt)*Mc**2
       
        return drag, Cd0
   
   
class horizTail():
    """
    This class contains the equations to determine an aircraft horizontal tail planform.
   
    # TODO: fix documentation
    """
    def __init__(self, wing, fuse):
        self.wing = wing
        self.fuse = fuse
       
       
    def planform(self, C, IIf, taper, LEsweep, AR):
        """
        This method determines the planform characteristics of a wing given its design parameters. It returns the values
        of these parameters as well as a plot of the wing plan view.
       
        # TODO: fix docs
        """
        # calculate I
        I = IIf*self.fuse.L
       
        # calculate area
        S = C*self.wing.mac*self.wing.S/I
       
        # calculate b
        b = np.sqrt(AR*S)
       
        # calculate root and tip chord
        cr = 2*b/(AR*(1 + taper))
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
       
        # save horiz tail info
        self.S = S
        self.AR = AR
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
   
   
    def drag(self, Mc, alt, tc, tcmax):
        """
        This method determines the drag characteristics of the planform determined in the planform() method. It returns
        the 0 lift drag coefficient of the tail as well as the total drag of the tail during cruise.
       
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
           
        Returns
        -------
        drag : float
            Total wing drag.
        Cd0 : float
            Wing zero lift drag coefficient.
        """
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
        F = 1.1*(1 + 0.6/tcmax*tc + 100*tc**4)*(1.34*(Mc**0.18)*np.cos(np.radians(tcsweep))**0.28)
       
        # now get wing CD0
        Cd0 = 1.05*Cf*Swet*F/self.wing.S
       
        # calc drag
        drag = Cd0*self.S*std.qMs(alt)*Mc**2
       
        return drag, Cd0
   
   
if __name__ == "__main__":
    plt.figure("Wing")
    wing = wing()
    wing.planform(714.3, 8, .35, 31.5)
   
    plt.figure("Fuse")
    fuse = fuse()
    fuse.PSCylGen(7, 11.5, [0.3, 0.2], 0.6)
   
    plt.figure("Vert. Tail")
    vtail = vertTail(wing, fuse)
    vtail.planform(0.06, 0.45, 0.55, 40, 1.2)
   
    plt.figure("Horiz. Tail")
    htail = horizTail(wing, fuse)
    htail.planform(0.69, 0.5, 0.4, 36.5, 5)
   
    plt.figure("Aircraft")
    plt.plot(fuse.plot[0], fuse.plot[1], "k")
    plt.plot(fuse.plot[0], -fuse.plot[1], "k")
    wloc = fuse.L/2 - wing.cr/2
    plt.plot(wing.plot[0] + wloc, wing.plot[1], "k")
    plt.plot(wing.plot[0] + wloc, -wing.plot[1], "k")
    tloc = fuse.L - htail.cr
    plt.plot(htail.plot[0] + tloc, htail.plot[1], "k")
    plt.plot(htail.plot[0] + tloc, -htail.plot[1], "k")
    plt.gca().set_aspect("equal")
    plt.xlabel("Length (ft)")
    plt.ylabel("Width (ft)")
    plt.grid()
   
    vdrag, vcd = vtail.drag(0.82, 36000, 0.12, 0.35)
    hdrag, hcd = htail.drag(0.82, 36000, 0.12, 0.35)
    wdrag, wcd = wing.drag(0.82, 36000, 0.12, 0.4, 0., 0.8, 0.8)
    _, fdrag = fuse.PSCylDrag(fuse, 0.82, 36000, wing.S)
    print(f"Total Drag: {vdrag + hdrag + wdrag + fdrag:.0f} lb")
    print(f"CD0: {vcd + hcd + wcd:.4f}")
    print(f"Design CD0: {1.2*(vcd + hcd + wcd):.4f}")
   
    plt.show()
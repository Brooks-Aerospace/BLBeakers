# Aircraft Wing Design Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet

"""
This code is a class called wing. It performs calculations based on given inputs to determine the planform, drag, and
performance characteristics of an aircraft wing.
"""

class wing():
    """
    This class contains the equations to determine an aircraft wing planform.
    
    Methods
    -------
    """
    
    def __init__(self, M, S, AR, ALE, tc, taper, Wo, Wf, qo, qf, Cl, alt, e):
        """
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
        
    def planform(self, S, AR, taper, LEsweep):
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
        MAC : float
            Mean aerodynamic chord.
        ymac : float
            Location of MAC on the wing.
        """
        
    def viscDrag():
        """
        
        """
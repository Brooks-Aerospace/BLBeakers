# Aircraft Weight Iteration Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet


import numpy as np
import sys
import os
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd, "..\\..\\"))
import stdatmos.standardAtmosphere as atmos

class itertow():
    """
    This class contains a function to iterate specific fuel consumption to achieve an aircraft weight breakdown
    throughout a mission.
    
    Methods
    -------
    itertow()
        Returns TSFC and weight at each portion of the mission.
    """
    
    def itertow(self, guess, Mc, rnge, alt, payload, thrust, ar, sf, loiter, reserve, trapped):
        """
        This method iteratively determines the TSFC required for a given mission, reserve, and gross weight and returns
        it and the aircraft weight at each phase in flight.
        
        Parameters
        ----------
        guess : float
            MTOGW first guess.
        Mc : float
            Cruise Mach number.
        rnge : float
            Aircraft range.
        alt : float
            Cruise altitude.
        payload : float
            Aircraft payload.
        thrust : float
            Aircraft thrust.
        ar : float
            Wing aspect ratio.
        sf : float
            Aircraft structure factor.
        loiter : float
            Reserve loiter time (mins).
        reserve : float
            Reserve fuel percentage.
        trapped : float
            Trapped fuel percentage.

        Returns
        -------
        """
        
        # start tsfc at 0
        tsfc = 0
        WTOf = np.empty(7)
        i = 0
        
        # iterate until guess agrees with estimate
        while WTOf[i] != guess:
            # initialize lists
            WTOest = np.empty(7)
            EWsurp = np.empty(7)
            wTO = np.empty(7)
            caccel = np.empty(7)
            cruise = np.empty(7)
            land = np.empty(7)
            Wtf = np.empty(7)
            EWavail = np.empty(7)
            reqEW = np.empty(7)
            
            # do 1 iteration
            WTOest[0] = 100000
            wTO[0] = 0.975*WTOest[0]
            if Mc < 1:
                caccel[0] = (1 - 0.04*Mc)*wTO[0]
                LoD = 10 + ar
            else:
                caccel[0] = (0.96 - 0.03*(Mc - 1))*wTO[0]
                LoD = 11*(1/Mc)**0.5
            cruise[0] = caccel[0]/np.exp(rnge*tsfc*6080/(LoD*Mc*atmos.standardAtmosphere.Aspeed(alt)[0]*3600))
            loiter[0] = cruise[0]/np.exp((loiter*tsfc)/(LoD*60))
            land[0] = loiter[0]*0.975
            Wtf[0] = (WTOest[0] - land[0])*(1 + (trapped + reserve)/100)
            EWavail[0] = WTOest[0] - Wtf[0] - payload
            reqEW[0] = WTOest[0]*sf
            WTOf[0] = Wtf[0] + reqEW[0] + payload
            EWsurp[0] = WTOest[0] - WTOf[0]
            
            # iterate until the surplus is 0
            #while EWsurp != 0:
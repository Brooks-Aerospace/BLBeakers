# Aircraft Weight Iteration Functions
# Slade Brooks
# spbrooks4@gmail.com
# this is a certified mark fellows excel sheet

import numpy as np
import pandas as pd
from utils.stdatmos import stdatmos


class weights():
    """
    This class contains functions to achieve an aircraft weight breakdown throughout a simple mission.
    
    Methods
    -------
    itertow()
        Returns weight at each portion of the mission.
    """
    
    def itertow(self, Mc, rnge, alt, payload, tsfc, ar, sf, loitert, reserve, trapped):
        """
        This method determines the aircraft weight at each phase in flight.
        
        Parameters
        ----------
        Mc : float
            Cruise Mach number.
        rnge : float
            Aircraft range.
        alt : float
            Cruise altitude.
        payload : float
            Aircraft payload.
        tsfc : float
            Thrust specific fuel consumption.
        ar : float
            Wing aspect ratio.
        sf : float
            Aircraft structure factor.
        loitert : float
            Reserve loiter time (mins).
        reserve : float
            Reserve fuel percentage.
        trapped : float
            Trapped fuel percentage.

        Returns
        -------
        df : pd.dataframe
            Pandas dataframe containing results arrays.
        """
        
        # initialize lists
        WTOf = np.zeros(5)
        WTOest = np.zeros(5)
        EWsurp = np.zeros(5)
        wTO = np.zeros(5)
        caccel = np.zeros(5)
        cruise = np.zeros(5)
        land = np.zeros(5)
        Wtf = np.zeros(5)
        EWavail = np.zeros(5)
        reqEW = np.zeros(5)
        loiter = np.zeros(5)
        i = 1
        
        std = stdatmos()
        
        # do 1 iteration
        WTOest[0] = 100000
        wTO[0] = 0.975*WTOest[0]
        if Mc < 1:
            caccel[0] = (1 - 0.04*Mc)*wTO[0]
            LoD = 10 + ar
        else:
            caccel[0] = (0.96 - 0.03*(Mc - 1))*wTO[0]
            LoD = 11*(1/Mc)**0.5
        cruise[0] = caccel[0]/np.exp(rnge*tsfc*6080/(LoD*Mc*std.Aspeed(alt)*3600))
        loiter[0] = cruise[0]/np.exp((loitert*tsfc)/(LoD*60))
        land[0] = loiter[0]*0.975
        Wtf[0] = (WTOest[0] - land[0])*(1 + (trapped + reserve)/100)
        EWavail[0] = WTOest[0] - Wtf[0] - payload
        reqEW[0] = WTOest[0]*sf
        WTOf[0] = Wtf[0] + reqEW[0] + payload
        EWsurp[0] = WTOest[0] - WTOf[0]
        
        # iterate until the surplus is 0
        while EWsurp[i - 1] != 0:
            if i==5:
                raise Exception("Too many iterations - check values")
            else:
                if i >= 2:
                    WTOest[i] = WTOest[i - 1] - EWsurp[i - 1]/((EWsurp[i - 1] - EWsurp[i - 2])/(WTOest[i - 1] - WTOest[i - 2]))
                elif i == 1:
                    WTOest[i] = WTOest[i - 1] - EWsurp[i - 1]
                
                wTO[i] = 0.975*WTOest[i]
                if Mc < 1:
                    caccel[i] = (1 - 0.04*Mc)*wTO[i]
                else:
                    caccel[i] = (0.96 - 0.03*(Mc - 1))*wTO[i]
                cruise[i] = caccel[i]/np.exp(rnge*tsfc*6080/(LoD*Mc*std.Aspeed(alt)*3600))
                loiter[i] = cruise[i]/np.exp((loitert*tsfc)/(LoD*60))
                land[i] = loiter[i]*0.975
                Wtf[i] = (WTOest[i] - land[i])*(1 + (trapped + reserve)/100)
                EWavail[i] = WTOest[i] - Wtf[i] - payload
                reqEW[i] = WTOest[i]*sf
                WTOf[i] = Wtf[i] + reqEW[i] + payload
                EWsurp[i] = WTOest[i] - WTOf[i]
                i += 1
        
        # output results
        df = pd.DataFrame({
                "TO Weight Est.": WTOest,
                "TO Weight Final": WTOf,
                "Surplus EW": EWsurp,
                "Startup/TO": wTO,
                "Climb and Accel": caccel,
                "Cruise": cruise,
                "Loiter": loiter,
                "Land": land,
                "Total Fuel Weight": Wtf,
                "Avail. EW": EWavail,
                "Req. EW": reqEW
            })
        pd.options.display.float_format = "{:.2f}".format
        
        return df


if __name__ == "__main__":
    itertow = weights()
    itertow.itertow(.82, 3800, 36000, 2600, 0.65, 8, 0.6, 45, 5, 1)
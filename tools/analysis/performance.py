# Aircraft Performance Calcs Class
# Slade Brooks
# brooksl@mail.uu.edu

from utils.stdatmos import stdAtmos
std = stdAtmos()
import numpy as np
import utils.units as uu


class performance():
    """
    Aircraft performance calculations class.
    """
    
    def __init__(self, ac):
        self.ac = ac
    
    
    def CL(self, alt:float, M:float, W:float, n:float=1):
        """
        Returns lift coefficient CL at alt (ft), M, weight (lb), and load factor (g's).
        """
        return n*W/(self.ac.S*std.qMs(alt)*M**2)
        
    
    def CD(self, alt:float, M:float, W:float, n:float=1):
        """
        Returns drag coefficient CD at alt (ft), M, weight (lb), and load factor (g's).
        """
        return self.ac.CD0 + self.ac.K*(self.CL(alt, M, W, n))**2
    
    
    def TR(self, alt:float, M:float, W:float):
        """
        Returns thrust required (lbf)/drag (lbf) at alt (ft) and M.
        """
        # account for wave drag if necessary
        if M > 0.7:
            Amax = (np.pi*self.ac.Dmax**2)/4
            cdw = 4*Amax/(np.pi*(self.ac.L/2)**2)
            Dwave = Amax*cdw*std.qMs(alt)*M**2
        else:
            Dwave = 0
        return self.CD(alt, M, W)*self.ac.S*std.qMs(alt)*M**2 + Dwave
    
    
    def LoDmax(self):
        """
        Returns max L/D ratio.
        """
        return np.sqrt(1/(4*self.ac.CD0*self.ac.K))
    
    
    def VLoDmax(self, alt, W):
        """
        Returns speed for max L/D ratio (kt) at alt (ft) and weight (lb).
        """
        return np.sqrt((2/std.rho(alt))*np.sqrt(self.ac.K/self.ac.CD0)*(W/self.ac.S))*uu.fps_to_kt
    
    
    def RoCmax(self, alt, T, W):
        """
        Returns max rate of climb (ft/s) at alt (ft) and weight (lb) with given thrust available (lbf).
        """
        Z = 1 + np.sqrt(1 + 3/(((T/W)**2)*(self.LoDmax()**2)))
        p = std.rho(alt)
        return (np.sqrt((W/self.ac.S)*Z/(3*p*self.ac.CD0)))*((T/W)**(3/2))* \
            (1 - (Z/6) - 3/(2*Z*((T/W)**2)*((self.LoDmax())**2)))/uu.s_to_min
    
    
    def VRoCmax(self, alt, T, W):
        """
        Returns speed (kt) for max RoC at alt (ft) and weight (lb) with given thrust available (lbf).
        """
        Z = 1 + np.sqrt(1 + 3/(((T/W)**2)*(self.LoDmax()**2)))
        p = std.rho(alt)
        return np.sqrt((T/self.ac.S)*Z/(3*p*self.ac.CD0))*uu.fps_to_kt
    
    
    def thetaMax(self, T, W):
        """
        Returns max climb angle (rad) at weight (lb) with given thrust available (lbf).
        """
        return np.arcsin(T/W - np.sqrt(4*self.ac.CD0*self.ac.K))
    
    
    def VThetaMax(self, alt, T, W):
        """
        Returns speed (kt) for max climb angle at alt (ft) and weight (lb) with given thrust available (lbf).
        """
        return np.sqrt((2/std.rho(alt))*(np.sqrt(self.ac.K/self.ac.CD0))*(W/self.ac.S)*np.cos(self.thetaMax(T, W))) \
            *uu.fps_to_kt
    
    
    def RoCThetaMax(self, alt, T, W):
        """
        Returns rate of climb (fpm) at max climb angle at alt (ft) and weight (lb) with given thrust available (lbf).
        """
        M = self.VThetaMax(alt, T, W)/std.velA(alt)
        V = self.VThetaMax(alt, T, W)*uu.kt_to_fps
        # return V*((T/W) - ((self.ac.CD0*std.qMs(alt)*M**2)/(W/self.ac.S) - (W*self.ac.K)/(self.ac.S*std.qMs(alt)*M**2))) \
        #     /uu.s_to_min
        return self.VThetaMax(alt, T, W)*uu.kt_to_fps*np.tan(self.thetaMax(T, W))/uu.s_to_min
    
    
    def RoC(self, V, alt, T, W):
        """
        Returns rate of climb (fpm) at speed (kt), alt (ft), and weight (lb) with given thrust available (lbf).
        """
        M = V/std.velA(alt)
        return V*(T - self.TR(alt, M, W))/W/uu.s_to_min
    
    
    def CL32oCDmax(self):
        """
        Returns max CL^3/2 /CD.
        """
        return (1/4)*(3/(self.ac.K*self.ac.CD0**(1/3)))**(3/4)
    
    
    def RoDmin(self, alt, W):
        """
        Returns minimum rate of descent (fpm) at alt (ft) and weight (lb).
        """
        return np.sqrt((2/(std.rho(alt)*self.CL32oCDmax()**2))*(W/self.ac.S))/uu.s_to_min
    
    
    def VRoDmin(self, alt, W):
        """
        Returns speed for minimum rate of descent (kt) at alt (ft) and weight (lb).
        """
        return 0.7598*self.VLoDmax(alt, W)
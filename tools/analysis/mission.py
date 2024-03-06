# Mission Segment Definition Class
# Slade Brooks
# brooksl@mail.uu.edu

import performance as perf
from utils.stdatmos import stdAtmos
std = stdAtmos()
import utils.units as uu


class mission():
    """
    Mission segment definition class.
    """
    
    def __init__(self, ac):
        """
        Parameters
        ----------
        ac : class
            Instance of aircraft class.
        """
        self.ac = ac
        self.perf = perf.performance(self.ac)
        
    
    def cruise(self, alt:float, M:float, TA:float, TSFC:float, rng:float, Wi:float):
        """
        Determine the time and final weight of a cruise segment.
        
        Parameters
        ----------
        alt : float
            Cruise altitude (ft).
        M : float
            Cruise mach number.
        TA : float
            Thrust available (lbf).
        TSFC : float
            Thrust specific fuel consumption (lbm/lbf-hr).
        rng : float
            Cruise range (nm).
        Wi : float
            Initial weight (lb).
        
        Returns
        -------
        t : float
            Cruise time (min).
        Wf : float
            Final weight (lb).
        """
        # ensure thrust is high enough for cruise
        if self.perf.TR(alt, M, Wi) > TA:
            print("--------------- !!! ---------------")
            print("Thrust required is more than thrust available!")
            print(f"TR: {self.perf.TR(alt, M, Wi):.0f} lbf, TA: {TA:.0f} lbf")
            print("--------------- !!! ---------------")
        
        # get V from M
        V = std.velA(alt)*M
        
        # calc time (hr)
        t = rng/V
        
        # calc final weight
        Wf = Wi - TSFC*self.perf.TR(alt, M, Wi)*t
        
        return t*uu.hr_to_min, Wf
    
    
    def maxClimb(self, alti:float, altf:float, TAi:float, TAf:float, TSFCi:float, TSFCf:float, Wi:float):
        """
        Determine the time, distance, and final weight of a climb segment at max climb performance.
        
        Parameters
        ----------
        alti : float
            Initial altitude (ft).
        altf : float
            Final altitude (ft).
        TAi : float
            Initial thrust available (lbf).
        TAf : float
            Final thrust available (lbf).
        TSFCi : float
            Initial thrust specific fuel consumption (lbm/lbf-hr).
        TSFCf : float
            Final thrust specific fuel consumption (lbm/lbf-hr).
        Wi : float
            Initial weight (lb).
        
        Returns
        -------
        t : float
            Time to climb (min).
        Wf : float
            Final weight (lb).
        rng : float
            Climb distance (nm).
        """
        # calc ave roc from max at each condition
        RoCAve = (self.perf.RoCmax(alti, TAi, Wi) + self.perf.RoCmax(altf, TAf, Wi))/2
        
        # also get average speed same deal
        Vave = (self.perf.VRoCmax(alti, TAi, Wi) + self.perf.VRoCmax(altf, TAf, Wi))/2

        # also ave TSFC
        TSFC = (TSFCi + TSFCf)/2
        
        # also ave TA
        TAave = (TAi + TAf)/2
        
        # calc time to climb (min)
        t = (altf - alti)/RoCAve
        
        # calc Wf
        Wf = Wi - TSFC*TAave*t*uu.min_to_hr
        
        # calc range
        rng = Vave*t*uu.min_to_hr
        
        return t, Wf, rng
    
    
    def maxAngleClimb(self, alti:float, altf:float, TAi:float, TAf:float, TSFCi:float, TSFCf:float, Wi:float):
        """
        Determine the time, distance, and final weight of a climb segment at max angle.
        
        Parameters
        ----------
        alti : float
            Initial altitude (ft).
        altf : float
            Final altitude (ft).
        TAi : float
            Initial thrust available (lbf).
        TAf : float
            Final thrust available (lbf).
        TSFCi : float
            Initial thrust specific fuel consumption (lbm/lbf-hr).
        TSFCf : float
            Final thrust specific fuel consumption (lbm/lbf-hr).
        Wi : float
            Initial weight (lb).
        
        Returns
        -------
        t : float
            Time to climb (min).
        Wf : float
            Final weight (lb).
        rng : float
            Climb distance (nm).
        """
        # calc ave roc at each condition
        RoCAve = (self.perf.RoCThetaMax(alti, TAi, Wi) + self.perf.RoCThetaMax(altf, TAf, Wi))/2
        
        # also get average speed same deal
        Vave = (self.perf.VThetaMax(alti, TAi, Wi) + self.perf.VThetaMax(altf, TAf, Wi))/2
        
        # also ave TSFC
        TSFC = (TSFCi + TSFCf)/2
        
        # also ave TA
        TAave = (TAi + TAf)/2
        
        # calc time to climb (min)
        t = (altf - alti)/RoCAve
        
        # calc Wf
        Wf = Wi - TSFC*TAave*t*uu.min_to_hr
        
        # calc range
        rng = Vave*t*uu.min_to_hr
        
        return t, Wf, rng
    
    
    def speedClimb(self, V:float, alti:float, altf:float, TAi:float, TAf:float, TSFCi:float, TSFCf:float, Wi:float):
        """
        Determine the time, distance, and final weight of a climb segment at a given speed.
        
        Parameters
        ----------
        V : float
            Speed (kt).
        alti : float
            Initial altitude (ft).
        altf : float
            Final altitude (ft).
        TAi : float
            Initial thrust available (lbf).
        TAf : float
            Final thrust available (lbf).
        TSFCi : float
            Initial thrust specific fuel consumption (lbm/lbf-hr).
        TSFCf : float
            Final thrust specific fuel consumption (lbm/lbf-hr).
        Wi : float
            Initial weight (lb).
        
        Returns
        -------
        t : float
            Time to climb (min).
        Wf : float
            Final weight (lb).
        rng : float
            Climb distance (nm).
        """
        # calc ave roc at each condition
        RoCAve = (self.perf.RoC(V, alti, TAi, Wi) + self.perf.RoC(V, altf, TAf, Wi))/2
        
        # also ave TSFC
        TSFC = (TSFCi + TSFCf)/2
        
        # also ave TA
        TAave = (TAi + TAf)/2
        
        # calc time to climb (min)
        t = (altf - alti)/RoCAve
        
        # calc Wf
        Wf = Wi - TSFC*TAave*t*uu.min_to_hr
        
        # calc range
        rng = V*t*uu.min_to_hr
        
        return t, Wf, rng
        
    
    def minDescend(self, alti:float, altf:float, Wi):
        """
        Determine the time and distance of a descent at minimum descent rate.
        
        Parameters
        ----------
        alti : float
            Initial altitude (ft).
        altf : float
            Final altitude (ft).
        Wi : float
            Initial weight (lb).
        
        Returns
        -------
        t : float
            Time to descend (min).
        Wf : float
            Final weight (lb).
        rng : float
            Descent distance (nm).
        """
        # calc ave rate of descent from min at each alt
        RoDAve = (self.perf.RoDmin(alti, Wi) + self.perf.RoDmin(alti, Wi))/2

        # calc ave speed
        Vave = (self.perf.VRoDmin(alti, Wi) + self.perf.VRoDmin(alti, Wi))/2
        
        # calc time to descend
        t = (alti - altf)/RoDAve

        # calc range
        rng = Vave*t*uu.min_to_hr
        
        # set Wf=Wi b/c assuming no fuel consumption in descent
        Wf = Wi
        
        return t, Wf, rng
    
    
    def accel(self, alt:float, Mi:float, Mf:float, TAi:float, TAf:float, TSFCi:float, TSFCf:float, Wi:float):
        """
        Determine the time, distance, and final weight to accelerate.
        
        Parameters
        ----------
        alt : float
            Altitude (ft).
        Mi : float
            Initial mach number.
        Mf : float
            Final mach number.
        TAi : float
            Initial thrust available (lbf).
        TAf : float
            Final thrust available (lbf).
        TSFCi : float
            Initial thrust specific fuel consumption (lbm/lbf-hr).
        TSFCf : float
            Final thrust specific fuel consumption (lbm/lbf-hr).
        Wi : float
            Initial weight (lb).
          
        Returns
        -------
        t : float
            Time to accelerate (min).
        Wf : float
            Final weight (lb).
        rng : float
            Acceleration distance (nm).
        """
        # ensure thrust is high enough for accel
        if self.perf.TR(alt, Mf, Wi) > TAf:
            print("--------------- !!! ---------------")
            print("Thrust required is more than thrust available!")
            print(f"TR: {self.perf.TR(alt, Mf, Wi):.0f} lbf, TA: {TAf:.0f} lbf")
            print("--------------- !!! ---------------")
        
        # calc ave acceleration from max at each speed
        Vdoti = 32.17405*(TAi - self.perf.TR(alt, Mi, Wi))/Wi
        Vdotf = 32.17405*(TAf - self.perf.TR(alt, Mf, Wi))/Wi
        Vdotave = (Vdoti + Vdotf)/2
        
        # calc ave speed and speed delta
        Vave = std.velA(alt)*(Mi + Mf)/2
        deltaV = std.Aspeed(alt)*(Mf - Mi)
        
        # calc ave thrust and TSFC
        TAave = (TAi + TAf)/2
        TSFC = (TSFCi + TSFCf)/2
        
        # calc time to accel
        t = deltaV/Vdotave
        
        # calc rng
        rng = Vave*t*uu.s_to_hr
        
        # calc Wf
        Wf = Wi - TSFC*TAave*t*uu.s_to_hr
        
        return t*uu.s_to_min, Wf, rng
    
    
    def decel(self, alt:float, Mi:float, Mf:float, Wi:float):
        """
        Determine the time and distance to decelerate.
        
        Parameters
        ----------
        alt : float
            Altitude (ft).
        Mi : float
            Initial mach number.
        Mf : float
            Final mach number.
        Wi : float
            Initial weight (lb).
        
        Returns
        -------
        t : float
            Time to decelerate (min).
        Wf : float
            Final weight (lb).
        rng : float
            Deceleration distance (nm).
        """
        # calc average deceleration from max at each speed
        Vdoti = -32.17405*self.perf.TR(alt, Mi, Wi)/Wi
        Vdotf = -32.17405*self.perf.TR(alt, Mf, Wi)/Wi
        Vdotave = (Vdoti + Vdotf)/2
        
        # calc ave speed and speed delta
        Vave = std.velA(alt)*(Mi + Mf)/2
        deltaV = std.velA(alt)*(Mf - Mi)
        
        # calc time to accel
        t = deltaV/Vdotave
        
        # calc rng
        rng = Vave*t*uu.s_to_hr
        
        # set Wf=Wi b/c assuming no fuel consumption during decel
        Wf = Wi
        
        return t*uu.s_to_min, Wf, rng
    
    
    def loiter(self, t:float, alt:float, TA:float, TSFC:float, Wi:float):
        """
        Determine the final weight and equivalent range of a loiter of given time.
        
        Parameters
        ----------
        t : float
            Loiter time (min).
        alt : float
            Altitude (ft).
        TA : float
            Thrust available (lbf).
        TSFC : float
            Thrust specific fuel consumption (lbm/lbf-hr).
        Wi : float
            Initial weight (lb).
            
        Returns
        -------
        t : float
            Loiter time (min).
        Wf : float
            Final weight (lb).
        rng : float
            Equivalent range (nm).
        """
        # calc Wf
        Wf = Wi - TSFC*TA*t*uu.min_to_hr
        
        # get speed and calc range
        V = self.perf.VLoDmax(alt, Wi)
        rng = V*t*uu.min_to_hr
        
        return t, Wf, rng
    
    
    def combat(self, t:float, pay:float, TA:float, TSFC:float, Wi:float):
        """
        Determine the final weight of a combat phase of given time with a specific expended payload.
        
        Parameters
        ----------
        t : float
            Combat time (min).
        pay : float
            Expended payload (lb).
        """
        # calc Wf
        Wf = Wi - TSFC*TA*t*uu.min_to_hr - pay
        
        return t, Wf
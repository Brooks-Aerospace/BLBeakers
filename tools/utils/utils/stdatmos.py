# Standard Atmosphere Class
# Slade Brooks
# spbrooks4@gmail.com
# i stole dis from class (notes)


import numpy as np
import utils.units as uu


class stdatmos():
    """
    This class contains all of the following standard atmosphere functions at a requested altitude.

    Methods
    -------
    tempF(alt)
        Return temperature at given alt in deg F.
    tempR(alt)
        Return temperature at given alt in deg R.
    tR(alt)
        Return temp ratio at given alt.
    pR(alt)
        Return pressure ratio at given alt.
    pres(alt)
        Return pressure at given alt in lbs/ft^2.
    rho(alt)
        Return density at given alt in slugs/ft^3.
    dR(alt)
        Return density ratio at given alt.
    sqrtDR(alt)
        Return square root of density ratio at given alt.
    qMs(alt)
        Returns the Q/M^2 at given alt in lbs/ft^2.
    spW(alt)
        Returns the specific weight at given alt in lbs/ft^3.
    Aspeed(alt)
        Returns the speed of sound at given alt in ft/s.
    velA(alt)
        Returns the speed of sound at given alt in kts.
    aR(alt)
        Returns the speed of sound ratio at given alt.
    VRkin(alt)
        Returns the kinematic viscosity at given alt in ft^2/s.
    """

    def tempF(self, alt:float):
        """
        This function returns the temperature in deg F of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.
        
        Returns
        -------
        tempF : float
            Temperature in deg F.
        """
        tempF = uu.r2degF(self.tempR(alt))

        return tempF

    def tempR(self, alt:float):
        """
        This function returns the temperature in deg R of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        tempR : float
            Temperature in deg R.
        """
        if alt <= 36089:
            tempR = 518.67 - 3.566*(alt/1000)
        elif alt <= 65617:
            tempR = 389.99

        return tempR

    def tR(self, alt:float):
        """
        This function returns the temperature ratio of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        tR : float
            Temperature ratio.
        """
        if alt <= 36089:
            tR = self.tempR(alt)/518.67
        elif alt <= 65617:
            tR = 389.99/518.67

        return tR

    def pR(self, alt:float):
        """
        This function returns the pressure ratio of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        pR : float
            Pressure ratio.
        """
        if alt <= 36089:
            pR = self.tR(alt)**5.2562
        elif alt <= 65617:
            pR = 0.223361*np.exp((-0.0481/1000)*(alt - 36089))

        return pR

    def pres(self, alt:float):
        """
        This function returns the pressure in lbs/ft^2 of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        pres : float
            Pressure in lbs/ft^2.
        """
        if alt <= 36089:
            pres = 2116.22*(self.tR(alt))**5.2562
        elif alt <= 65617:
            pres = 2116.22*self.pR(alt)

        return pres

    def rho(self, alt:float):
        """
        This function returns the density in slugs/ft^3 of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        rho : float
            Density in slugs/ft^3.
        """
        if alt <= 65617:
            rho = 0.0023769*(self.pR(alt)/self.tR(alt))

        return rho

    def dR(self, alt:float):
        """
        This function returns the density ratio of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        dR : float
            Density ratio.
        """
        if alt <= 65617:
            dR = self.pR(alt)/self.tR(alt)

        return dR

    def sqrtDR(self, alt:float):
        """
        This function returns the square root of the density ratio of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        sqrtDR : float
            Square root of density ratio.
        """
        if alt <= 65617:
            sqrtDR = np.sqrt(self.dR(alt))

        return sqrtDR

    def qMs(self, alt:float):
        """
        This function returns the dynamic pressure over mach squared of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        qMs : float
            Q/M^2 in lbs/ft^2.
        """
        if alt <= 65617:
            qMs = 1481.354*self.pR(alt)

        return qMs

    def spW(self, alt:float):
        """
        This function returns the specific weight in lbs/ft^3 of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        spW : float
            Specific weight in lbs/ft^3.
        """
        if alt <= 65617:
            spW = 32.1740484*self.rho(alt)

        return spW

    def Aspeed(self, alt:float):
        """
        This function returns the speed of sound in ft/s of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        Aspeed : float
            Speed of sound in ft/s.
        """
        if alt <= 65617:
            Aspeed = 1116.45*np.sqrt(self.tR(alt))

        return Aspeed

    def velA(self, alt:float):
        """
        This function returns the speed of sound in kts of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        velA : float
            Speed of sound in kts.
        """
        if alt <= 65617:
            velA = (3600/6076.4)*self.Aspeed(alt)

        return velA
    
    def aR(self, alt:float):
        """
        This function returns the speed of sound ratio of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        aR : float
            Speed of sound ratio.
        """
        if alt <= 65617:
            aR = self.Aspeed(alt)/self.Aspeed(0)

        return aR

    def VRkin(self, alt:float):
        """
        This function returns the kinematic viscosity in ft^2/s of a US standard day at the requested altitude.

        Parameters
        ----------
        alt : float
            Altitude in feet.

        Returns
        -------
        VRkin : float
            Kinematic viscosity in ft^2/s.
        """
        if alt <= 65617:
            VRkin = ((0.226968*10**(-7))*(self.tempR(alt)**1.5))/(self.rho(alt)*(self.tempR(alt)+198.73))

        return VRkin


# testing
if __name__ == "__main__":
    std = stdatmos()

    temp = std.tempF(1000)
    print(temp)

    # verified
    # print(std.tempF(1000))
    # print(std.tempR(1000))
    # print(std.tempF(42000))
    # print(std.tempR(42000))

    # verified
    # print(std.tR(1000))
    # print(std.tR(42000))
    # print(std.pR(1000))
    # print(std.pR(42000))

    # verified
    # print(std.pres(1000))
    # print(std.pres(42000))
    # print(std.rho(1000))
    # print(std.rho(42000))

    # verified
    # print(std.dR(1000))
    # print(std.dR(42000))
    # print(std.sqrtDR(1000))
    # print(std.sqrtDR(42000))
    # print(std.qMs(1000))
    # print(std.qMs(42000))

    # verified
    # print(std.spW(1000))
    # print(std.spW(42000))
    # print(std.Aspeed(1000))
    # print(std.Aspeed(42000))
    # print(std.velA(1000))
    # print(std.velA(42000))
    # print(std.VRkin(1000))
    # print(std.VRkin(42000))
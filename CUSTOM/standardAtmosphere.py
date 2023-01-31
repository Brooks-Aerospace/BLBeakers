# Standard Atmosphere Class
# Slade Brooks
# spbrooks4@gmail.com
# i stole dis from class

"""
This code is a class called standardAtmosphere. It performs calculations
and returns standard atmosphere values at a specific altitude. Each
atmospheric property is its own function within the class, and there is
an SI conversion function as well.

It includes the properties:
    temp (F)
    temp (R)
    temp ratio
    pres ratio
    pressure
    density
    density ratio
    sqrt density ratio
    q over mach^2
    specific weight
    speed of sound (ft/s)
    speed of sound (kts)
    kinematic viscosity
"""

import numpy as np


class standardAtmosphere():
    """
    This class contains all of the following standard atmosphere
    functions at a requested altitude and a unit conversion function.

    :Methods:
        tempF
        tempR
        tR
        pR
        pres
        rho
        dR
        sqrtDR
        qMs
        spW
        Aspeed
        velA
        VRkin
        convertUnits
    """

    def tempF(self, alt:float):
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF: temp in deg F
        :rtype: float
        """
        tempF = self.tempR(alt) - 459.67

        return tempF, "deg F"

    def tempR(self, alt:float):
        """
        This function returns the temperature in deg R
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempR: temp in deg R
        :rtype: float
        """
        if alt <= 36089:
            tempR = 518.67 - 3.566*(alt/1000)
        elif alt <= 65617:
            tempR = 389.99

        return tempR, "deg R"

    def tR(self, alt:float):
        """
        This function returns the temperature ratio
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempRatio: temp ratio
        :rtype: float
        """
        if alt <= 36089:
            tR = self.tempR(alt)/518.67
        elif alt <= 65617:
            tR = 389.99/518.67

        return tR

    def pR(self, alt:float):
        """
        This function returns the pressure ratio
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns pR: pressure ratio
        :rtype: float
        """
        if alt <= 36089:
            pR = self.tR(alt)**5.2562
        elif alt <= 65617:
            pR = 0.223361*np.exp((-0.0481/1000)*(alt - 36089))

        return pR

    def pres(self, alt:float):
        """
        This function returns the pressure in lbs/ft^2
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns pres: pressure in lbs/ft^2
        :rtype: float
        """
        if alt <= 36089:
            pres = 2116.22*(self.tR(alt))**5.2562
        elif alt <= 65617:
            pres = 2116.22*self.pR(alt)

        return pres, "lbs/ft^2"

    def rho(self, alt:float):
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns rho: density in slugs/ft^3
        :rtype: float
        """
        if alt <= 65617:
            rho = 0.0023769*(self.pR(alt)/self.tR(alt))

        return rho, "slugs/ft^3"

    def dR(self, alt:float):
        """
        This function returns the density ratio
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns dR: density ratio
        :rtype: float
        """
        if alt <= 65617:
            dR = self.pR(alt)/self.tR(alt)

        return dR

    def sqrtDR(self, alt:float):
        """
        This function returns the square root of the density
        ratio of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns sqrtDr: density ratio
        :rtype: float
        """
        if alt <= 65617:
            sqrtDR = np.sqrt(self.dR(alt))

        return sqrtDR

    def qMs(self, alt:float):
        """
        This function returns the dynamic pressure over
        mach squared of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns qms: Q/M^2 in lbs/ft^2
        :rtype: float
        """
        if alt <= 65617:
            qMs = 1481.354*self.pR(alt)

        return qMs, "lbs/ft^2"

    def spW(self, alt:float):
        """
        This function returns the specific weight in lbs/ft^3
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns spw: specific weight in lbs/ft^3
        :rtype: float
        """
        if alt <= 65617:
            spW = 32.1740484*self.rho(alt)

        return spW, "lbs/ft^3"

    def Aspeed(self, alt:float):
        """
        This function returns the speed of sound in ft/s
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns Aspeed: speed of sound in ft/s
        :rtype: float
        """
        if alt <= 65617:
            Aspeed = 1116.45*np.sqrt(self.tR(alt))

        return Aspeed, "ft/s"

    def velA(self, alt:float):
        """
        This function returns the speed of sound in kts
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns velA: speed of sound in kts
        :rtype: float
        """
        if alt <= 65617:
            velA = (3600/6076.4)*self.Aspeed(alt)

        return velA, "kts"

    def VRkin(self, alt:float):
        """
        This function returns the kinematic viscosity
        in ft^2/s of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns VRkin: kinematic viscosity in ft^2/s
        :rtype: float
        """
        if alt <= 65617:
            VRkin = ((0.226968*10**(-7))*(self.tempR(alt)**1.5))/(self.rho(alt)*(self.tempR(alt)+198.73))

        return VRkin, "ft^2/s"

    def convertUnits(freedomUnits):
        """
        This function converts the input value to SI
        units given its value and units.

        :param freedomUnits: standardAtmosphere function @ requested altitude
        :returns convertedVal: converted units in SI
        :rtype: float
        """

        val = freedomUnits[0]
        units = freedomUnits[1]

        if units == "deg F":
            val = (val - 32)*(5/9)
            units = "deg C"
        elif units == "deg R":
            val = (val-491.67)*(5/9)
            units = "deg C"
        elif units == "lbs/ft^2":
            val = val*47.880172
            units = "Pa"
        elif units == "slugs/ft^3":
            val = val*515.379
            units = "kg/m^3"
        elif units == "lbs/ft^3":
            val = val*16.0185
            units = "kg/m^3"
        elif units == "ft/s":
            val = val/3.281
            units = "m/s"
        elif units == "kts":
            val = val/1.94384
            units = "m/s"
        elif units == "ft^2/s":
            val = val/10.764
            units = "m^2/s"


# testing
if __name__ == "__main__":
    std = standardAtmosphere()

    print(std.tempF(1000)[0])
    print(std.tempF(1000)[1])

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
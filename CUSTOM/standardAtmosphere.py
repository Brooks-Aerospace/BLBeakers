# Brooks Aerospace Design Suite VSP API Commands
# Slade Brooks
# spbrooks4@gmail.com
# i stole dis from class

"""
This code is a class called standardAtmosphere. It performs calculations
and returns standard atmosphere values at a specific altitude. Each
atmospheric property is its own function within the class, and there is
an SI conversion function as well.

It includes the properties:

"""

import numpy as np

class standardAtmosphere():
    """
    This class contains all of the following standard atmosphere
    properties at a requested altitude and a unit conversion function.


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

        return tempF

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

        return tempR

    def tempRatio(self, alt:float):
        """
        This function returns the temperature ratio
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempRatio: temp ratio
        :rtype: float
        """
        if alt <= 36089:
            tempRatio = self.tempR(alt)/518.67
        elif alt <= 65617:
            tempRatio = 389.99/518.67

        return tempRatio

    def presRatio(self, alt:float):
        """
        This function returns the pressure ratio
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns presRatio: pressure ratio
        :rtype: float
        """
        if alt <= 36089:
            presRatio = self.tempRatio(alt)**5.2562
        elif alt <= 65617:
            presRatio = 0.223361*np.exp((-0.0481/1000)*(alt - 36089))

        return presRatio

    def pres(self, alt:float):
        """
        This function returns the pressure in lbs/ft^2
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns pres: pressure in lbs/ft^2
        :rtype: float
        """
        if alt <= 36089:
            pres = 2116.22*(self.tempRatio(alt))**5.2562
        elif alt <= 65617:
            pres = 2116.22*self.presRatio(alt)

        return pres

    def rho(self, alt:float):
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns rho: density in slugs/ft^3
        :rtype: float
        """
        if alt <= 65617:
            rho = 0.0023769*(self.presRatio(alt)/self.tempRatio(alt))

        return rho

    def densRatio(self, alt:float):
        """
        This function returns the density ratio
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns densRatio: density ratio
        :rtype: float
        """
        if alt <= 65617:
            densRatio = self.presRatio(alt)/self.tempRatio(alt)

        return densRatio

    def sqrtDR(self, alt:float):
        """
        This function returns the square root of the density
        ratio of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns sqrtDr: density ratio
        :rtype: float
        """
        sqrtDR = np.sqrt(self.densRatio(alt))

        return sqrtDR

    def QMS():
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF, units: temp in deg F
        :rtype: float
        :returns units: units of value
        :rtype: string
        """

    def SPW():
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF, units: temp in deg F
        :rtype: float
        :returns units: units of value
        :rtype: string
        """

    def Aspeed():
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF, units: temp in deg F
        :rtype: float
        :returns units: units of value
        :rtype: string
        """

    def velA():
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF, units: temp in deg F
        :rtype: float
        :returns units: units of value
        :rtype: string
        """

    def VRkin():
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF, units: temp in deg F
        :rtype: float
        :returns units: units of value
        :rtype: string
        """

    def convertUnits():
        """
        This function returns the temperature in deg F
        of a US standard day at the requested altitude.

        :param alt: float, altitude in feet
        :returns tempF, units: temp in deg F
        :rtype: float
        :returns units: units of value
        :rtype: string
        """
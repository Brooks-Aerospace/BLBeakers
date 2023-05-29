"""
# Aircraft Datasheet Class
# Slade Brooks
# spbrooks4@gmail.com

This code is a class called acDatasheet. It takes inputs of
various aircraft information and saves it to be accessed for
performance calculations our outputting to other software.

It includes:
    surface sizes, dimensions, and locations
    lift and drag info
    max q/M
"""

class acDatasheet:
    """
    This class takes inputs of various aircraft
    information and saves it to be accessed for
    performance calculations our outputting to
    other software.

    Attributes
    ----------
    name : string
        Aircraft name.
    
    Methods
    -------
    """

    def __init__(self, name:str):
        """
        Initializes the datasheet class with the
        aircraft name.

        Parameters
        ----------
        name : string
            Aircraft name.
        """
        self.name = name

    def generalInputs(self):
        """
        
        """
        self.cd0 = float(input("Cd0:"))
        self.clMaxClean = float(input("CLmax clean:"))
        self.clMaxTO = float(input("CLmax T/O:"))
        self.clMaxLand = float(input("CLmax landing:"))
        self.numeng = int(input("# of engines:"))
        self.Tsls = float(input("sea level thrust:"))
        self.SFCsls = float(input("sea level specific fuel consumption:"))
        self.maxGs = float(input("max g's:"))
        self.minGs = float(input("min g's:"))
        self.maxKEAS = float(input("max KEAS:"))
        self.maxQ = float(input("max Q:"))
        self.maxM = float(input("max mach:"))
        self.maxAlt = float(input("max altitude:"))
        self.maxTOGW = float(input("max takeoff gross weight:"))
        self.maxFuel = float(input("max fuel weight:"))

    def fuseInputs(self):
        """
        
        """

    def wingInputs(self):
        """
        
        """

if __name__ == "__main__":

    cheese = acDatasheet("steve")

    cheese.generalInputs()
# Brooks Aerospace Design Suite VSP API Commands
# Slade Brooks
# spbrooks4@gmail.com
# it only took me 2 hours to get the API working this time!

"""
This code is the collection of classes, functions, and other fun stuff
that runs the VSP UI in BADS. The classes and functions inside can be repurposed
for use outside of the UI.

It runs through the OpenVSP API (docs found below). It requires an input file.
The standard workflow is to create the vehicle geometry in VSP, then utilize this
code to optimize the design.

Link to VSP API Documentation:
http://openvsp.org/api_docs/latest/index.html

Notes:
- anything starting with "_" is NOT for the user to use
- nothing has units - must track on your own and be consistent
"""

import openvsp as vsp
import os


class VSPCraft:
    """
    This class opens a craft in VSP to perform design and analysis.
    The nested classes will be used to obtain the features of the craft
    for use in calculations.
    """

    def __init__(self, VSPFilename:str):
        """
        This function opens and checks the VSP file.

        :param_VSPFilename: VSP file path
        """

        # checks and opens VSP file
        vsp.VSPCheckSetup()
        VSPFilename = self._cleanPath(dirtyPath=VSPFilename)
        vsp.ReadVSPFile(file_name=VSPFilename)  

        return

    class craftObject:
        """
        This class defines an object and its properties from a VSP model.
        It can be any static object on the craft: engine, propeller, motor that
        needs a defined weight, position, or more.
        """

        def __init__(self, objectName:str, weight:float):
            """
            This function creates the craft object.

            :param_objectName: object title in VSP
            :param_weight: weight of the object (w/o units)
            """

            # find named geometry
            self.craftObject = VSPCraft._findGeom(geomName=objectName)

            # sets craft object params from inputs
            self.weight = weight
            self.position = []
            self.position.append(vsp.GetParmVal(self.craftObject,"X_Rel_Location","XForm"))
            self.position.append(vsp.GetParmVal(self.craftObject,"Y_Rel_Location","XForm"))
            self.position.append(vsp.GetParmVal(self.craftObject,"Z_Rel_Location","XForm"))

    class simpleWing:
        """
        This class defines a simple (1 section) wing from a VSP model.
        It gathers the wing properties and can make changes to them.
        """

        def __init__(self, wingName:str, weight:float):
            """
            This function gets the wing parameters from the given VSP model.

            :param_wingName: wing title in VSP
            :param_weight: weight of the object (w/o units)
            """

    @staticmethod
    def _findGeom(geomName:str):
        """
        This function finds an object in a VSP file given its name.
        """
        return vsp.FindGeomsWithName(geomName)[0]

    @staticmethod
    def _cleanPath(dirtyPath:str):
        """
        This function takes a filepath with abbreviated home directory,
        expands it, and normalizes it for OS usage.
        """
        # check for list of paths to clean
        if type(dirtyPath) is list:
            # step through list and perform _cleanpath
            return [VSPCraft._cleanpath(path) for path in dirtyPath] 
        else:
            # expand "~"
            cleanPath = os.path.expanduser(dirtyPath)

            # normalize "/" direction based on os preference
            cleanPath = os.path.normpath(cleanPath)

        # gimme a clean path!
        return cleanPath


# test script, only activates when this file is run
if __name__ == "__main__":
    # do stuff
    print("running")

    testVehicle = VSPCraft(VSPFilename="~/BrooksAeroDesignSuite/OpenVSP/vspfiletest.vsp3")
    fuse = testVehicle.craftObject(objectName="fuse", weight=100.0)
    
    print(fuse.weight)
    print(fuse.position)
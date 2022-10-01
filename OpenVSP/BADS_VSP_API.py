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

class craftObject:
    """
    This class defines an object and its properties from a VSP model.
    It can be any static object on the craft: engine, propeller, motor that
    needs a defined weight, position, or more.
    """

    def __init__(self, VSPFilename:str, objectName:str, weight:float):
        """
        This function creates the craft object.

        param_VSPFilename: VSP file path
        param_objectName: object title in VSP
        param_weight: weight of the object (w/o units)
        """

        # checks and opens VSP file
        vsp.VSPCheckSetup()
        VSPFilename = _cleanPath(self, dirtyPath=VSPFilename)
        vsp.ReadVSPFile(file_name=VSPFilename)

        # find named geometry
        self.craftObject = _findGeom(geomName=objectName)

        # sets craft object params from inputs
        self.weight = weight
        self.position = []
        self.position.append(vsp.GetParmVal(self.craftObject,"X_Rel_Location","XForm"))
        self.position.append(vsp.GetParmVal(self.craftObject,"Y_Rel_Location","XForm"))
        self.position.append(vsp.GetParmVal(self.craftObject,"Z_Rel_Location","XForm"))

def _findGeom(geomName:str):
    """
    This function finds an object in a VSP file given its name.
    """
    return vsp.FindGeomsWithName(geomName)[0]

def _cleanPath(self, dirtyPath:str):
    """
    This function takes a filepath with abbreviated home directory,
    expands it, and normalizes it for OS usage.
    """
    # check for list of paths to clean
    if type(dirtyPath) is list:
         # step through list and perform _cleanpath
        return [self._cleanpath(path) for path in dirtyPath] 
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

    fuse = craftObject(VSPFilename="~/BrooksAeroDesignSuite/OpenVSP/vspfiletest.vsp3",
                     objectName="fuse", weight=100.0)
    
    print(fuse.weight)
    print(fuse.position)
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


class VSPCraft():
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
        self.VSPFilename = VSPFilename  

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

            # sets craft object params
            self.weight = weight
            self.position = []
            self.position.append(vsp.GetParmVal(self.craftObject,"X_Rel_Location","XForm"))
            self.position.append(vsp.GetParmVal(self.craftObject,"Y_Rel_Location","XForm"))
            self.position.append(vsp.GetParmVal(self.craftObject,"Z_Rel_Location","XForm"))

    @staticmethod
    def save(filename:str):
        """
        This function saves the file.
        """
        filename = VSPCraft._cleanPath(filename)
        vsp.WriteVSPFile(filename)

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
        # check for list
        if type(dirtyPath) is list:
            # clean list
            return [VSPCraft._cleanpath(path) for path in dirtyPath] 
        else:
            # expand "~"
            cleanPath = os.path.expanduser(dirtyPath)

            # normalize "/" direction based on os preference
            cleanPath = os.path.normpath(cleanPath)

        # gimme a clean path!
        return cleanPath

class simpleWing(VSPCraft):
    """
    This class defines a simple (1 section) wing from a VSP model.
    It gathers the wing properties and can make changes to them.
    The wing can have different airfoils and chords at the root and tip.
    """

    def __init__(self, wingName:str, weight:float):
        """
        This function gets the wing parameters from the given VSP model.

        :param_wingName: wing title in VSP
        :param_weight: weight of the object (w/o units)
        """

        # find named wing
        self.simpleWing = VSPCraft._findGeom(geomName=wingName)

        # sets wing params
        self.weight = weight
        self.position = []
        self.position.append(vsp.GetParmVal(self.simpleWing,"X_Rel_Location","XForm"))
        self.position.append(vsp.GetParmVal(self.simpleWing,"Y_Rel_Location","XForm"))
        self.position.append(vsp.GetParmVal(self.simpleWing,"Z_Rel_Location","XForm"))
        self.span = vsp.GetParmVal(self.simpleWing,"TotalSpan","WingGeom")
        self.area = vsp.GetParmVal(self.simpleWing,"TotalArea","WingGeom")
        self.incidence = vsp.GetParmVal(self.simpleWing,"Twist","XSec_0")
        self.rootChord = vsp.GetParmVal(self.simpleWing,"Root_Chord","XSec_1")
        self.tipChord = vsp.GetParmVal(self.simpleWing,"Tip_Chord","XSec_1")
        self.sweep = vsp.GetParmVal(self.simpleWing,"Sweep","XSec_1")
        self.twist = vsp.GetParmVal(self.simpleWing,"Twist","XSec_1")
        self.dihedral = vsp.GetParmVal(self.simpleWing,"Dihedral","XSec_1")

    def updateAirfoils(self, rootNACA:bool, tipNACA:bool, rootNACAthick:float, tipNACAthick:float,
                        newRootFoil:str, newTipFoil:str, rootChord:float, tipChord:float):
        """
        This function updates the airfoil of the simplewing. It supports
        NACA airfoils at the root and tip or af files at the root and tip.

        :param_rootNACA: flag for a NACA 4 series vs airfoil file at root
        :param_tipNACA: flag for a NACA 4 series vs airfoil file at tip
        :param_rootNACAthick: T/C of NACA 4 series
        :param_tipNACAthick: T/C of NACA 4 series
        :param_newRootFoil: af file path for root
        :param_newTipFoil: af file path for tip
        :param_rootChord: new root chord
        :param_tipChord: new tip chord
        """

        # update root
        # check NACA flag
        if rootNACA == True:
            # do 4 series update
            vsp.ChangeXSecShape(vsp.GetXSecSurf(self.simpleWing, 1), 0, vsp.XS_FILE_AIRFOIL)

            vsp.Update()
            self.save(self.VSPFilename)


# test script, only activates when this file is run
if __name__ == "__main__":
    # do stuff
    print("running")

    testVehicle = VSPCraft(VSPFilename="~/BrooksAeroDesignSuite/OpenVSP/vspfiletest.vsp3")

    wing1 = simpleWing(wingName="mainwing", weight=100.0)
    testVehicle.save('vsp_output.vsp3')

    # vsp tracks stuff, classes can be separate
    # thx devon



    testVehicle.addComponent(simpleWing(wingName="mainwing", weight=100.0))


    # fuse = testVehicle.craftObject(objectName="fuse", weight=100.0)
    wing = simpleWing(wingName="mainwing", weight=100.0)
    
    # print(fuse.weight)
    # print(fuse.position)

    wing.updateAirfoils(True, True, 8, 8, None, None, None, None)

    # print(wing.area)
    # print(wing.dihedral)
    # print(wing.incidence)
    # print(wing.position)
    # print(wing.rootChord)
    # print(wing.tipChord)
    # print(wing.area)
    # print(wing.span)
    # print(wing.sweep)
    # print(wing.twist)
    # print(wing.weight)
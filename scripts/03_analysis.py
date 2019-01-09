import processing
from  qgis.utils import *
import os
from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (QgsProcessingAlgorithm,
       QgsProcessingParameterFeatureSource,
       QgsProcessingParameterCrs,
       QgsProcessingParameterFolderDestination,
       QgsProject,
       QgsProcessingOutputVectorLayer,
       QgsProcessingOutputNumber)

class PreProcessing(QgsProcessingAlgorithm):

    # Initialize variables for input parameters of GUI.
    # Add all your input parameters here
    PARAMETER1 = ''
    OUTPUTFOLDER = ''
    DUMMYOUTPUT = "0"

    # Don't edit this
    def __init__(self):
        super().__init__()

    # Replace "Template" with the name of your script
    def name(self):
        return "03 - Analysis"

    # Replace "template" with the name of your script
    def tr(self, text):
        return QCoreApplication.translate("03 - Analysis", text)

    # Replace "template" with the name of your script
    def displayName(self):
        return "03 - Analysis"

    # Replace "Examples" with the name of your group of scripts
    def group(self):
        return self.tr("My Analysis")

    # Replace "examples" with the name of your group of scripts
    def groupId(self):
        return "myanalysis"

    # Don't edit this
    def createInstance(self):
        return type(self)()

    def initAlgorithm(self, config=None):
        # Add all input variables here
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.PARAMETER1, "Parameter 1"))
        self.addParameter(QgsProcessingParameterFolderDestination(
            self.OUTPUTFOLDER, "Output directory"))

        # Add all output varaibles here (optional, you may also just keep the dummy variable)
        # Keep this dummy output variable, if you don't want any other outputs
        self.addOutput(QgsProcessingOutputNumber(self.DUMMYOUTPUT, ""))

    def processAlgorithm(self, parameters, context, feedback):

        # Extract input parameters provided by the user
        # ---------------------------------------------
        # Add all your input parameters here
        parameter1 = self.parameterAsString(
            parameters,
            self.PARAMETER1,
            context
        )
        outputDirectory = self.parameterAsString(
            parameters,
            self.OUTPUTFOLDER,
            context
        )

        # Add algorithms here
        # -----------------

        # Define output file path -----------------------------------------------
        outputfile = os.path.join(outputDirectory, "outputfile.shp")

        # Set parameters for algorithm and execute it
        params = {
            # Add all necessary parameters here.
            # Check processing.algorithmHelp("name_of_algorithm") for information on parameters
            #"INPUT": ...,
            #"OUTPUT": ....
        }
        # Execute the algorithm
        algorithmOutput = processing.run("native:fixgeometries", params, context=context, feedback=feedback)

        # Extract output of algorithm result. This is usually a string variable containing a path to a file that has been created.
        output = algorithmOutput["OUTPUT"]

        # If you don't want to specify an output, then just keep this return statement as it is
        return {self.DUMMYOUTPUT : "0"}

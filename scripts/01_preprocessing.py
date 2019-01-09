import processing
from  qgis.utils import *
import os
from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (QgsProcessingAlgorithm,
       QgsProcessingParameterFeatureSource,
       QgsProcessingParameterCrs,
       QgsProcessingParameterFolderDestination,
       QgsProject,
       QgsProcessingOutputVectorLayer)

class PreProcessing(QgsProcessingAlgorithm):
    DAMSELFISH_FILE = 'DAMSELFISH_FILE'
    REEF_FILE = 'REEF_FILE'
    CRS = None
    OUTPUT_DIRECTORY = 'None'
    OUTPUT1 = ""
    OUTPUT2 = ""

    def __init__(self):
        super().__init__()

    def name(self):
        return "01 - Preprocessing"

    def tr(self, text):
        return QCoreApplication.translate("01 - Preprocessing", text)

    def displayName(self):
        return "01 - Preprocessing"

    def group(self):
        return self.tr("My Analysis")

    def groupId(self):
        return "myanalysis"

    def createInstance(self):
        return type(self)()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.DAMSELFISH_FILE, "Damselfish file"))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.REEF_FILE, "Reef file"))
        self.addParameter(QgsProcessingParameterCrs(
            self.CRS, "Target Coorindate Reference System"))
        self.addParameter(QgsProcessingParameterFolderDestination(
            self.OUTPUT_DIRECTORY, "Output folder"))
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT1, ""))
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT2, ""))

    def processAlgorithm(self, parameters, context, feedback):

        # INPUT PARAMETERS
        # ---------------------
        # Damselfish species distribution file
        #self.DAMSELFISH_FILE = "/Users/chludwig/Documents/teaching/SE_FOSSGIS/SE_FOSSGIS_WS1819/exercises/ex_07/Data/DAMSELFISH_distributions.shp"
        # Coral reef file
        #self.REEF_FILE = "/Users/chludwig/Documents/teaching/SE_FOSSGIS/SE_FOSSGIS_WS1819/exercises/ex_07/Data/Global_Threats/Integrated_Future/rf_int_2050_poly.shp"
        # output directory
        #self.OUTPUT_DIRECTORY = "/Users/chludwig/Documents/teaching/SE_FOSSGIS/SE_FOSSGIS_WS1819/exercises/ex_07/output"
        # target CRS
        #self.CRS = "EPSG:4326"

        # Extract input parameters provided by the user
        # ---------------------------------------------

        damselfish_file = self.parameterAsString(
            parameters,
            self.DAMSELFISH_FILE,
            context
        )
        reef_file = self.parameterAsString(
            parameters,
            self.REEF_FILE,
            context
        )
        directory = self.parameterAsString(
            parameters,
            self.OUTPUT_DIRECTORY,
            context
        )
        crs = self.parameterAsCrs(
            parameters,
            self.CRS,
            context)


        # FIX GEOMETRIES
        # -----------------
        #processing.algorithmHelp("qgis:fieldcalculator")
        def no_post_process(alg, context, feedback):
            pass

        # Fix damselfish layer ---------------------------------------------------------
        output_damselfish_fixed = os.path.join(directory, "damselfish_fixed.shp")

        # Set parameters for algorithm and execute it
        params = {
            "INPUT": damselfish_file,
            "OUTPUT": output_damselfish_fixed
        }
        algorithmOutput = processing.run("native:fixgeometries", params, context=context, feedback=feedback)

        # Fix reef layer ---------------------------------------------------------------
        output_reefs_fixed = os.path.join(directory, "reefs_fixed.shp")

        # Set parameters for algorithm and execute it
        params = {
            "INPUT": reef_file,
            "OUTPUT": output_reefs_fixed
        }
        algorithmOutput = processing.run("native:fixgeometries", params, context=context, feedback=feedback)

        # REPROJECT TO COMMON CRS
        # -------------------------
        #processing.algorithmHelp("native:reprojectlayer")

        # Path to output file
        output_reefs_reprojected = os.path.join(directory, "reefs_reprojected.shp")

        # Set parameters for algorithm
        params = {
            "INPUT": output_reefs_fixed,
            "TARGET_CRS": crs,
            "OUTPUT": output_reefs_reprojected
        }

        # Execute algorithm
        algorithmOutput = processing.run("native:reprojectlayer", params, context=context, feedback=feedback)

        # Path to output file
        output_damselfish_reprojected = os.path.join(directory, "damselfish_reprojected.shp")

        # Set parameters for algorithm
        params = {
            "INPUT": output_damselfish_fixed,
            "TARGET_CRS": crs,
            "OUTPUT": output_damselfish_reprojected
        }

        # Execute algorithm
        algorithmOutput = processing.run("native:reprojectlayer", params, context=context, feedback=feedback)

        return {self.OUTPUT1: output_reefs_reprojected, self.OUTPUT2: output_damselfish_reprojected}

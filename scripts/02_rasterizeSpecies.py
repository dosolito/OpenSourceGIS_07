import os
import processing

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessingAlgorithm,
       QgsProcessingParameterFeatureSource,
       QgsProcessingParameterCrs,
       QgsProcessingParameterFolderDestination,
       QgsProject,
       QgsProcessingOutputVectorLayer,
       QgsProcessingOutputFolder)

class RasterizeSpecies(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    DAMSELFISH_FILE = 'Da'
    REEF_FILE = "ff"
    CRS = None
    OUTPUT_DIRECTORY = ""

    def __init__(self):
        super().__init__()

    def name(self):
        return "02 Rasterize Species"

    def tr(self, text):
        return QCoreApplication.translate("02 - Rasterize Species", text)

    def displayName(self):
        return self.tr("02 - Rasterize Species")

    def group(self):
        return self.tr("My Analysis")

    def groupId(self):
        return "myanalysis"

    def shortHelpString(self):
        return self.tr("Extracts and rasterizes species")

    def helpUrl(self):
        return "https://qgis.org"

    def createInstance(self):
        return type(self)()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.DAMSELFISH_FILE, "Damselfish file"))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.REEF_FILE, "Reef file"))
        #self.addParameter(QgsProcessingParameterField(
        #    self.attribute, "Attribute"))
        self.addParameter(QgsProcessingParameterFolderDestination(
            self.OUTPUT_DIRECTORY, "Output folder"))
        self.addOutput(QgsProcessingOutputFolder(self.OUTPUT, ""))

    def processAlgorithm(self, parameters, context, feedback):

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
        destination = self.parameterAsString(
            parameters,
            self.OUTPUT_DIRECTORY,
            context
        )
        crs = self.parameterAsCrs(
            parameters,
            self.CRS,
            context)

        attribute = "BINOMIAL"
        targetSpecies = ["Chromis cyanea", "Microspathodon dorsalis", "Stegastes acapulcoensis"]
        '''
        # Intersect with threat areas
        output_intersection = os.path.join(destination, "species_reefs_intersected.shp")
        # Set parameters for algorithm
        params = {
            "INPUT": damselfish_file,
            "OVERLAY": reef_file,
            "OUTPUT": output_intersection,
            "OVERLAY_FIELDS": ["THREAT"],
            "INPUT_FIELDS": ["BINOMIAL"]
        }
        algorithmOutput = processing.run("native:intersection", params, context=context, feedback=feedback)
        '''

        for species in targetSpecies:
            # Create path to output file
            output_species= os.path.join(destination,species.replace(" ","_") + ".shp")

            # Store paramters for algorithm
            params = {
                "INPUT": damselfish_file,
                "FIELD": attribute,
                "OPERATOR": 0,
                "VALUE": species,
                "OUTPUT": output_species
            }
            # Execute algorithm
            algorithmOutput = processing.run("native:extractbyattribute", params, context=context, feedback=feedback)

            # Rasterize species
            output_rasterized= os.path.join(destination, species + "_rasterized.tif")
            # Set parameters for algorithm
            params = {
                "INPUT": output_species,
                "BURN": "1",
                "UNITS": 1,
                "WIDTH": 1000,
                "HEIGHT": 1000,
                "EXTENT": output_species,
                "OUTPUT": output_rasterized,
            }
            algorithmOutput = processing.run("gdal:rasterize", params, context=context, feedback=feedback)


        return {self.OUTPUT: destination}

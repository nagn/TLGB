#!/usr/bin/env python
import sys, os, glob, tempfile, json
import settings
import file_handling.json_handler as json_handler
import file_handling.legacy_file_handler as legacy
from PyQt4 import QtCore, QtGui
from TLGB import Ui_MapEditor
import wizard
from widgets import EntityButtonLabel, EntityScrollArea, MapEntityLabel, EntityScrollArea, GamemodeSelector, MapPreviewScene
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_MapEditor()
        self.ui.setupUi(self)
        
        #The current executing directory of the python script
        self.directory = sys.path[0]
        self.mapDirectory = os.path.join(self.directory , "sprites/floaton/cp_floaton.png")
        self.tempDirectory = tempfile.mkdtemp()
        self.mapBackgroundImage, self.mapWallmaskImage = None, None
        #Load the default configuration (All entity types)
        self.entityTypes = json_handler.generate_all_entities()
        
        #Create the gamemode selecting comboBox before the scroll area, so it is on top
        self.gamemodeSelector = GamemodeSelector(self)
        self.ui.verticalLayoutEntity.addWidget(self.gamemodeSelector)
        
        #Generate the Scroll Area of the Entity Browser
        self.ui.entityScrollArea = EntityScrollArea(self)
        self.ui.verticalLayoutEntity.addWidget(self.ui.entityScrollArea)
        
        self.mapZoomLevel = 6
        
        
        self.legacyEntityDict = json.loads(open("config/legacy_types.json").read())
        #these are a list of entities to be ignored while that option is toggled
        self.redundantEntityList = json.loads(open("config/redundant_legacy_types.json").read())
        
        #Create the mapPreviewScene
        self.ui.mapPreviewScene = MapPreviewScene(self.redundantEntityList, self)
        self.ui.verticalLayout.addWidget(self.ui.mapPreviewScene.views()[0])
        
        #Create the Entity Grid
        self.entityGrid = QtGui.QGridLayout()
        
        #Create a dummy widget for us to easily to set to the grid Layout
        self.ui.containerWidget = QtGui.QWidget()
        self.ui.containerWidget.setLayout(self.entityGrid)
        #Add to the Scroll Area
        self.ui.entityScrollArea.setWidget(self.ui.containerWidget)
        
        #Generate the ToolBar
        self.addToolbar('icons\gb\icon_new.png', 'New', self.newMap, QtGui.QKeySequence.New)
        self.addToolbar('icons\gb\open.png', 'Open', self.loadMap, QtGui.QKeySequence.Open)
        self.addToolbar('icons\gb\save.png', 'Save', None, QtGui.QKeySequence.Save)
        self.addToolbar('icons\gb\delete.png', 'Exit', QtGui.qApp.quit, QtGui.QKeySequence.Quit)
        self.addToolbar('icons\gb\shrink.png', 'Zoom Out', self.scaleDown, QtGui.QKeySequence.ZoomOut)
        self.addToolbar('icons\gb\expand.png', 'Zoom In', self.scaleUp, QtGui.QKeySequence.ZoomIn)
        self.addToolbar('icons\gb\equal.png', 'Zoom Reset', self.scaleReset)
        
        self.wallmaskVisible = True
        self.backgroundVisible = True
        self.redundantEntitiesVisible = True
        self.basicEntitiesVisible = True
        
        self.ui.actionWallmask.triggered.connect(self.toggleWallmaskVisibility)
        self.ui.actionBackground.triggered.connect(self.toggleBackgroundVisibility)
        self.ui.actionBasicEntities.triggered.connect(self.toggleBasicEntityVisibility)
        self.ui.actionRedundantEnt.triggered.connect(self.toggleRedundantEntityVisibility)
        
        #Load all the json files in settings.GAMEMOES_PATH
        self.gamemodeList = []
        for gamemode in(glob.glob( os.path.join(settings.GAMEMODES_PATH, '*.json'))):
            self.gamemodeList.append(os.path.splitext(os.path.basename(gamemode))[0])
        self.gamemodeSelector.addItems(self.gamemodeList)
        
        #load the json file and handle it, default the current one
        self.loadGamemode(os.path.join(settings.GAMEMODES_PATH , str(self.gamemodeSelector.currentText()) + ".json"))
        
        self.cachedEntities = {}
    def loadMap (self, mapDirectory):
        #Load Map, and grab the map data
        self.mapBackground = None
        self.mapWallmask = None
        self.mapEntities = None
        entities = []
        self.renderingEntityList = []
        self.mapDirectory = QtGui.QFileDialog.getOpenFileName(
           filter = "PNG (*.png)"
        )
        if self.mapDirectory != "":
            try:
                entities, wallmask = legacy.extractLevelData(self.mapDirectory, os.path.join(self.tempDirectory,"wallmask.png"), True)
                self.mapWallmask = QtGui.QImage(os.path.join(self.tempDirectory,"wallmask.png"))
                self.mapBackground = QtGui.QImage(self.mapDirectory)
                for iteration in range(len(entities)):
                    x, y =  entities[iteration][1]
                    mapEntityPixmap , (xOffset, yOffset), entityName = self.createMapEntPixmap(entities[iteration][0])
                    self.renderingEntityList.append((mapEntityPixmap, (x,y), (-xOffset, -yOffset), entityName))
            except legacy.NoData:
                #As there is no leveldata, only load the background
                self.mapBackground = QtGui.QImage(self.mapDirectory)
        self.ui.mapPreviewScene.loadMap(self.mapBackground, self.mapWallmask, self.renderingEntityList)
    def loadGamemode(self, gamemodePath):
        gamemodeConfig = json_handler.load_gamemode(os.path.join(sys.path[0],gamemodePath))
        gamemodeCategories = gamemodeConfig['categories']
        gamemodeEntities = gamemodeConfig['entities']
        entityList = []
        #we have to nest categories on the outside to conserve the order
        for category in gamemodeCategories:
            for entity in self.entityTypes:
                if entity.attributes['category'] == category:
                    entityList.append(entity)
        for gamemodeEntity in gamemodeEntities:
            for entity in self.entityTypes:
                if entity.attributes['id'] == gamemodeEntity:
                    entityList.append(entity)
        
        #generate the Labels
        self.labelList = []
        for iteration, entity in enumerate(entityList):
            newEntity = EntityButtonLabel(entity.attributes.copy(), self)
            self.labelList.append(newEntity)
            self.entityGrid.addWidget(newEntity, iteration, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.ui.entityScrollArea.resetEntities()
    def scaleDown(self):
        self.mapZoomLevel /= 1.2
        self.ui.mapPreviewScene.changeScale(self.mapZoomLevel)
    def scaleUp(self):
        self.mapZoomLevel *= 1.2
        self.ui.mapPreviewScene.changeScale(self.mapZoomLevel)
    def scaleReset(self):
        self.mapZoomLevel = 6
        self.ui.mapPreviewScene.changeScale(self.mapZoomLevel)
    def newMap(self):
        self.showWizard()
    def addToolbar(self, iconPath, name, function = None, shortcut = None):
        
        action = QtGui.QAction(QtGui.QIcon(iconPath), name, self)
        if shortcut:
            action.setShortcut(shortcut)
        self.toolbar = self.addToolBar(name)
        if function:
            action.triggered.connect(function)
        self.toolbar.addAction(action)
    def showWizard(self):
        self.mapWizard = wizard.MapWizard()
        #self.mapWizard.FinishButton.setAutoDefault (False)
    def toggleWallmaskVisibility(self):
        if self.ui.actionWallmask.isChecked():
            self.wallmaskVisible = True
        else:
            self.wallmaskVisible = False
        self.ui.mapPreviewScene.changeVisiblity()
    def toggleBasicEntityVisibility(self):
        if self.ui.actionBasicEntities.isChecked():
            self.basicEntitiesVisible = True
        else:
            self.basicEntitiesVisible = False
        self.ui.mapPreviewScene.changeVisiblity()
    def toggleRedundantEntityVisibility(self):
        if self.ui.actionRedundantEnt.isChecked():
            self.redundantEntitiesVisible = True
        else:
            self.redundantEntitiesVisible = False
        self.ui.mapPreviewScene.changeVisiblity()
    def toggleBackgroundVisibility(self):
        if self.ui.actionBackground.isChecked():
            self.backgroundVisible = True
        else:
            self.backgroundVisible = False
        self.ui.mapPreviewScene.changeVisiblity()

    def createMapEntPixmap(self, entityFileName):
        #Memoized for speed
        if not entityFileName in self.cachedEntities:
            self.cachedEntities[entityFileName] = self.returnMapEntPixmap(entityFileName)
        return self.cachedEntities[entityFileName]
    def returnMapEntPixmap(self, entityFileName):
        image = QtGui.QImage(os.path.join(self.legacyEntityDict[entityFileName]["filename"],"image 0.png"))
        xOffset = int(self.legacyEntityDict[entityFileName]["mapImageOrigin"]["x"])
        yOffset = int(self.legacyEntityDict[entityFileName]["mapImageOrigin"]["y"])
        pixmap = QtGui.QPixmap.fromImage(image)
        return(pixmap, (xOffset,yOffset), entityFileName)
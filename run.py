#!/usr/bin/env python
from __future__ import print_function, division
import sys, os
import glob
import constants, json_handler
from PyQt4 import QtCore, QtGui
from TLGB import Ui_MapEditor
import wizard
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MapEditor()
        self.ui.setupUi(self)
        
        #The current executing directory of the python script
        self.directory = sys.path[0]
        self.map_directory = os.path.join(self.directory , "sprites/montane/montane.png")
        
        #Load the default configuration (All entity types)
        self.entityTypes = json_handler.generate_all_entities()
        
        #Generate the Scroll Area of the Map Previewer
        self.ui.scrollAreaMap = ScrollAreaMap(self)
        self.ui.verticalLayout.addWidget(self.ui.scrollAreaMap)
        
        #Lets get manual control of those scroll bars, baby
        self.ui.scrollBarHorizontal = QtGui.QScrollBar()
        self.ui.scrollBarVertical = QtGui.QScrollBar()
        self.ui.scrollAreaMap.setHorizontalScrollBar(self.ui.scrollBarHorizontal)
        self.ui.scrollAreaMap.setVerticalScrollBar(self.ui.scrollBarVertical)
        
        #Create the gamemode selecting comboBox before the scroll area, so it is on top
        self.gamemodeSelector = GamemodeSelector(self)
        self.ui.verticalLayoutEntity.addWidget(self.gamemodeSelector)
        
        #Generate the Scroll Area of the Entity Browser
        self.ui.scrollAreaEntity = ScrollAreaEntity(self)
        self.ui.verticalLayoutEntity.addWidget(self.ui.scrollAreaEntity)
        
        #Generate the Map Preview Label
        self.ui.mapPreview = MapPreview()
        self.ui.scrollAreaMap.setWidget(self.ui.mapPreview)
        
        self.mapZoomLevel = 6
        #Load Map, and grab the map data
        self.mapWidth, self.mapHeight, mapImage = self.load_map(self.map_directory)
        
        #Lets save the img for later use
        self.mapImage = mapImage
        
        #Convert the QImage into QPixmap
        mapBackground = QtGui.QPixmap.fromImage(self.mapImage)
        
        #Scale the map to 6x
        self.ui.mapPreview.setScaledContents(True)
        mapBackground = mapBackground.scaled(QtCore.QSize(self.mapWidth*self.mapZoomLevel,self.mapHeight*self.mapZoomLevel),QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
        self.ui.mapPreview.setPixmap(mapBackground)
        self.ui.mapPreview.setFixedSize(mapBackground.size())
        
        #Create the Entity Grid
        self.entityGrid = QtGui.QGridLayout()
        
        #Create a dummy widget for us to easily to set to the grid Layout
        self.containerWidget = QtGui.QWidget()
        self.containerWidget.setLayout(self.entityGrid)
        #Add to the Scroll Area
        self.ui.scrollAreaEntity.setWidget(self.containerWidget)
        
        #Generate the ToolBar
        self.add_toolbar('icons\gb\icon_new.png', 'New', None, QtGui.QKeySequence.New)
        self.add_toolbar('icons\gb\open.png', 'Open', None, QtGui.QKeySequence.Open)
        self.add_toolbar('icons\gb\save.png', 'Save', None, QtGui.QKeySequence.Save)
        self.add_toolbar('icons\gb\delete.png', 'Exit', QtGui.qApp.quit, QtGui.QKeySequence.Quit)
        self.add_toolbar('icons\gb\shrink.png', 'Zoom Out', self.scale_down, QtGui.QKeySequence.ZoomOut)
        self.add_toolbar('icons\gb\expand.png', 'Zoom In', self.scale_up, QtGui.QKeySequence.ZoomIn)
        self.add_toolbar('icons\gb\equal.png', 'Zoom Reset', self.scale_reset)
        
        #Load all the json files in constants.GAMEMOES_PATH
        self.gamemodeList = []
        for gamemode in(glob.glob( os.path.join(constants.GAMEMODES_PATH, '*.json'))):
            self.gamemodeList.append(os.path.splitext(os.path.basename(gamemode))[0])
        self.gamemodeSelector.addItems(self.gamemodeList)
        
        #load the json file and handle it, default the current one
        self.load_gamemode(os.path.join(constants.GAMEMODES_PATH , str(self.gamemodeSelector.currentText()) + ".json"))
    
    def load_map (self, map_directory):
        #We create a QImage in order to fetch map information
        img = QtGui.QImage(self.map_directory)
        return (img.width(), img.height(), img)
    def load_gamemode(self, gamemodePath):
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
            newEntity = EntityLabel(entity.attributes.copy(), self)
            self.labelList.append(newEntity)
            self.entityGrid.addWidget(newEntity, iteration, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            self.ui.scrollAreaEntity.resetEntities()
    def scale_down(self):
        self.mapZoomLevel -= 3
        if self.mapZoomLevel <1:
            self.mapZoomLevel = 3
        #Store the current offset
        currentHorizontalProportion = float(self.ui.scrollBarHorizontal.sliderPosition())/max(1.0, float(self.ui.scrollBarHorizontal.maximum()))
        currentVerticalProportion = float(self.ui.scrollBarVertical.sliderPosition())/max(1.0 ,float(self.ui.scrollBarVertical.maximum()))
        pixmap = self.ui.mapPreview.pixmap()
        pixmap = pixmap.scaledToHeight(self.mapHeight*self.mapZoomLevel, False)
        self.ui.mapPreview.setPixmap(pixmap)
        self.ui.mapPreview.setFixedSize(pixmap.size())
        #Set a new offset
        self.ui.scrollBarHorizontal.setSliderPosition(int(currentHorizontalProportion*self.ui.scrollBarHorizontal.maximum()))
        self.ui.scrollBarVertical.setSliderPosition(int(currentVerticalProportion*self.ui.scrollBarVertical.maximum()))
        self.show_wizard()
    def scale_up(self):
        self.mapZoomLevel += 3
        if self.mapZoomLevel >12:
            self.mapZoomLevel = 12
        currentHorizontalProportion = float(self.ui.scrollBarHorizontal.sliderPosition())/max(1.0 ,float(self.ui.scrollBarHorizontal.maximum()))
        currentVerticalProportion = float(self.ui.scrollBarVertical.sliderPosition())/max(1.0 ,float(self.ui.scrollBarVertical.maximum()))
        
        pixmap = self.ui.mapPreview.pixmap()
        pixmap = pixmap.scaledToHeight(self.mapHeight*self.mapZoomLevel, False)
        self.ui.mapPreview.setPixmap(pixmap)
        self.ui.mapPreview.setFixedSize(pixmap.size())
        
        self.ui.scrollBarHorizontal.setSliderPosition(int(currentHorizontalProportion*self.ui.scrollBarHorizontal.maximum()))
        self.ui.scrollBarVertical.setSliderPosition(int(currentVerticalProportion*self.ui.scrollBarVertical.maximum()))
    def scale_reset(self):
        self.mapZoomLevel = 6
        currentHorizontalProportion = float(self.ui.scrollBarHorizontal.sliderPosition())/max(1.0, float(self.ui.scrollBarHorizontal.maximum()))
        currentVerticalProportion = float(self.ui.scrollBarVertical.sliderPosition())/max(1.0 ,float(self.ui.scrollBarVertical.maximum()))
        
        pixmap = self.ui.mapPreview.pixmap()
        pixmap = pixmap.scaledToHeight(self.mapHeight*self.mapZoomLevel, False)
        self.ui.mapPreview.setPixmap(pixmap)
        self.ui.mapPreview.setFixedSize(pixmap.size())
        
        self.ui.scrollBarHorizontal.setSliderPosition(int(currentHorizontalProportion*self.ui.scrollBarHorizontal.maximum()))
        self.ui.scrollBarVertical.setSliderPosition(int(currentVerticalProportion*self.ui.scrollBarVertical.maximum()))
        
    def add_toolbar(self, iconPath, name, function = None, shortcut = None):
        
        action = QtGui.QAction(QtGui.QIcon(iconPath), name, self)
        if shortcut:
            action.setShortcut(shortcut)
        self.toolbar = self.addToolBar(name)
        if function:
            action.triggered.connect(function)
        self.toolbar.addAction(action)
    def show_wizard(self):
        self.mapWizard = wizard.MapWizard()
        #self.mapWizard.FinishButton.setAutoDefault (False)
class EntityLabel (QtGui.QLabel):
    def __init__(self, attributes, myForm, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.attributes = attributes
        
        self.setMouseTracking(True)
        
        #icon for entity
        img = QtGui.QImage(os.path.join(sys.path[0], str(self.attributes['gbImage'])))
        width = img.width()
        height = img.height()
        icon = QtGui.QPixmap.fromImage(img)
        
        #We scale the icons to be doubled. We might make this user adjustable later on
        self.setScaledContents(True)
        icon = icon.scaled(QtCore.QSize(width*2,height*2),QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
        self.setPixmap(icon)
        #A callback so we can reference main form variables elsewhere
        self.form = myForm
        self.setStatusTip(self.attributes['humanReadableName'])
        
    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL("clicked(PyQt_PyObject)"), event)
        try:
            print(self.attributes['humanReadableName'])
        except KeyError:
            print("attribute 'humanReadableName' does not exist!")
    def enterEvent(self, event):
        app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    
    def leaveEvent(self, event):
        app.restoreOverrideCursor()
    def clicked(self):
        print("whatever")
class MapPreview (QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)

class ScrollAreaMap (QtGui.QScrollArea):
    def __init__(self, form, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
        self.form = form
    def sizeHint(self):
        return QtCore.QSize(500,700)
    def resizeEvent(self, event):
        pass

class ScrollAreaEntity (QtGui.QScrollArea):
    def __init__(self, myForm, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
        self.form = myForm
        #Add 15 pixels to compensate for the vertical scroll bar
        self.setMinimumWidth(constants.ENTITY_SPACING*2 + constants.ENTITY_WIDTH + 15)
        #We NEVER want the horizontal scroll bar
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    def sizeHint(self):
        return QtCore.QSize(100,-1)
    def resizeEvent(self, event):
        self.resetEntities()
        
    def resetEntities(self):
        myWidth = self.frameRect().width()
        entityWidth = constants.ENTITY_WIDTH
        entitySpacing = constants.ENTITY_SPACING
        
        #Destroy our old layout (Hopefully it's being garbage collected)
        self.form.containerWidget = QtGui.QWidget()
        self.form.entityGrid = QtGui.QGridLayout()
        
        #Compute how many collumns we can fit in here
        if int(myWidth) // int(entityWidth+entitySpacing*2) > 1:
            numberOfCollumns = (int(myWidth) // int(entityWidth+entitySpacing))
        else:
            numberOfCollumns = 1
        
        currentCollumn = 0
        currentRow = 0
        for iteration, currentEntity in enumerate(self.form.labelList):
            self.form.entityGrid.addWidget(self.form.labelList[iteration], currentRow, currentCollumn, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            #If we have reached the end of a collumn, advance a row
            #(note that 0 modulous anything is 0, so it must be compensated for)
            if currentCollumn+1 == numberOfCollumns:
                advancingRow = True
            else:
                advancingRow = False
            currentCollumn = (currentCollumn + 1) % numberOfCollumns
            if advancingRow == True:
                currentRow += 1

        #update the scroll area
        self.form.containerWidget.setLayout(self.form.entityGrid)
        self.form.ui.scrollAreaEntity.setWidget(self.form.containerWidget)
class GamemodeSelector(QtGui.QComboBox):
    def __init__(self, myForm, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self.form = myForm
        QtCore.QObject.connect(self, QtCore.SIGNAL("currentIndexChanged(QString)"), self.changedMode)
        self.setStatusTip("Select a Game Mode")
    def changedMode(self):
        currentText = str(self.currentText())
        self.form.load_gamemode(os.path.join(constants.GAMEMODES_PATH , currentText + ".json"))
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
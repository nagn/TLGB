#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import os, sys
import settings
class EntityButtonLabel (QtGui.QLabel):
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
class MapEntityLabel(QtGui.QLabel):
    def __init__(self, pixmap, x, y, parent=None):
        super(MapEntityLabel, self).__init__(parent)
        self.setPixmap(pixmap)
        self.x = x
        self.y = y
class EntityScrollArea (QtGui.QScrollArea):
    def __init__(self, myForm, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
        self.form = myForm
        #Add 15 pixels to compensate for the vertical scroll bar
        self.setMinimumWidth(settings.ENTITY_SPACING*2 + settings.ENTITY_WIDTH + 15)
        #We NEVER want the horizontal scroll bar
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    def sizeHint(self):
        return QtCore.QSize(100,-1)
    def resizeEvent(self, event):
        self.resetEntities()
        
    def resetEntities(self):
        myWidth = self.frameRect().width()
        entityWidth = settings.ENTITY_WIDTH
        entitySpacing = settings.ENTITY_SPACING
        
        #Destroy our old layout (Hopefully it's being garbage collected)
        self.form.ui.containerWidget = QtGui.QWidget()
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
        self.form.ui.containerWidget.setLayout(self.form.entityGrid)
        self.form.ui.entityScrollArea.setWidget(self.form.ui.containerWidget)
class GamemodeSelector(QtGui.QComboBox):
    def __init__(self, myForm, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self.form = myForm
        QtCore.QObject.connect(self, QtCore.SIGNAL("currentIndexChanged(QString)"), self.changedMode)
        self.setStatusTip("Select a Game Mode")
    def changedMode(self):
        currentText = str(self.currentText())
        self.form.loadGamemode(os.path.join(settings.GAMEMODES_PATH , currentText + ".json"))
        
class MapPreviewScene(QtGui.QGraphicsScene):
    def __init__(self, backgroundImage, wallmaskImage, renderingList, redundantLegacyList, form, parent=None):
        super(MapPreviewScene, self).__init__(parent)
        
        self.backgroundImage = backgroundImage
        self.background = self.addPixmap(QtGui.QPixmap(backgroundImage))
        self.background.setZValue(-2)
        
        #self.wallmaskImage = wallmaskImage
        self.wallmask = self.addPixmap(QtGui.QPixmap(wallmaskImage))
        self.wallmask.setZValue(-1)
        QtCore.QObject.connect(self, QtCore.SIGNAL("changed(QList<QRectF>)"), self.updateScene)
        self.form = form
        self.renderingList = renderingList
        self.view = QtGui.QGraphicsView(self)
        self.view.scale(self.form.mapZoomLevel,self.form.mapZoomLevel)
        self.view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.view.setMouseTracking(True)
        for renderedEntity in self.renderingList:
            x, y = renderedEntity[1]
            xOffset, yOffset = renderedEntity[2]
            #The QGraphicsItem added will default to 0,0 for its coordinates. We should override it.
            entity = self.addPixmap(renderedEntity[0])
            #reverse the transformations that scaling the view does for the entities
            viewTransform = self.view.transform().inverted()
            #The boolean result is the second part of the tuple. We don't care if we're passing the identity or not, so here
            entity.setTransform(viewTransform[0])
            entity.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
            entity.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
            entity.setPos(entity.mapToScene(x,y))
            entity.setOffset(xOffset, yOffset)
            entity.setOpacity(0.65)
            #Special attributes we set for the sake of sorting
            entity.setData(0, renderedEntity[3])
            entity.setZValue(1)
            entity.setToolTip(renderedEntity[3])
        self.redundantLegacyList = redundantLegacyList
    def updateScene(self):
        pass
    def changeVisiblity(self):
        if self.form.wallmaskVisible == False:
            self.wallmask.hide()
        else:
            self.wallmask.show()
        self.wallmask.update()
        if self.form.backgroundVisible == False:
            self.background.hide()
        else:
            self.background.show()
        self.background.update()
        
        redundantEntities =[item for item in self.items() if item.data(0) in self.redundantLegacyList
                            and item != self.wallmask and item != self.background]
        basicEntities = [item for item in self.items() if item.data(0) not in self.redundantLegacyList
                         and item != self.wallmask and item != self.background]
        
        for basicEntity in basicEntities:
            if self.form.basicEntitiesVisible:
                basicEntity.show()
            else:
                basicEntity.hide()
            basicEntity.update()
        for redundantEntity in redundantEntities:
            if self.form.redundantEntitiesVisible:
                redundantEntity.show()
            else:
                redundantEntity.hide()
            redundantEntity.update()
        
    def changeScale(self, scaleLevel):
        viewTransform = self.view.transform()
        viewTransform.reset()
        viewTransform = viewTransform.scale(scaleLevel,scaleLevel)
        self.view.setTransform(viewTransform)

#!/usr/bin/python -d
 
import sys, os
from PyQt4 import QtCore, QtGui
from TLGB import Ui_MapEditor

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MapEditor()
        self.ui.setupUi(self)
        
        #The current executing directory of the python script
        self.directory = sys.path[0]
        self.map_directory = self.directory + "/sprites/montane/montane.png"
        
        #Generate the Scroll Area of the Map Previewer
        self.ui.scrollAreaMap = ScrollAreaMap()
        self.ui.verticalLayout.addWidget(self.ui.scrollAreaMap)
        
        #Generate the Map Preview Label
        self.ui.mapPreview = MapPreview()
        self.ui.scrollAreaMap.setWidget(self.ui.mapPreview)
        
        #Load Map, and grab the map data
        self.map_width, self.map_height, mapBackground = self.load_map(self.map_directory)
        #Scale the map to 6x
        self.ui.mapPreview.setScaledContents(True)
        mapBackground = mapBackground.scaledToHeight(self.map_height*6,False)
        self.ui.mapPreview.setPixmap(mapBackground)
        self.ui.mapPreview.setFixedSize(mapBackground.size())
        
        #Generate the Entity Grid
        EntityGrid = QtGui.QGridLayout()
        #Generate the Corresponding Entities
        for i in range(30):
            EntityGrid.addWidget(EntityLabel(), i, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            #There doesn't seem to be a way to set the default row height, so we have to do it per row
            EntityGrid.setRowMinimumHeight(i, 64)
        #Create a dummy widget for us to easily to set to the scroll area
        containerWidget = QtGui.QWidget()
        containerWidget.setLayout(EntityGrid)
        #Add to the scroll Area
        self.ui.scrollAreaEntity.setWidget(containerWidget)
        
        #Generate the ToolBar
        self.add_toolbar('icons\gb\newicon.png', 'New', None, QtGui.QKeySequence.New)
        self.add_toolbar('icons\gb\open.png', 'Open', None, QtGui.QKeySequence.Open)
        self.add_toolbar('icons\gb\save.png', 'Save', None, QtGui.QKeySequence.Save)
        self.add_toolbar('icons\gb\delete.png', 'Exit', QtGui.qApp.quit, QtGui.QKeySequence.Quit)
        self.add_toolbar('icons\gb\shrink.png', 'Zoom Out', self.scale_down, QtGui.QKeySequence.ZoomIn)
        self.add_toolbar('icons\gb\expand.png', 'Zoom In', self.scale_down, QtGui.QKeySequence.ZoomOut)
        self.add_toolbar('icons\gb\equal.png', 'Zoom Resest', self.scale_reset)

    def load_map (self, map_directory):
        #We create a QImage in order to fetch map information
        img = QtGui.QImage(self.map_directory)
    
        #Convert the QImage into a QPixmap
        mapBackground = QtGui.QPixmap.fromImage(img)
        return (img.width(), img.height(), mapBackground)
    def scale_down(self):
        
        pixmap = QtGui.QPixmap(self.map_directory)
        pixmap = pixmap.scaledToHeight(self.map_height*3, False)
        self.ui.mapPreview.setPixmap(pixmap)
        self.ui.mapPreview.setFixedSize(pixmap.size())
        
    def scale_up(self):
    
        pixmap = QtGui.QPixmap(self.map_directory)
        pixmap = pixmap.scaledToHeight(self.map_height*9, False)
        self.ui.mapPreview.setPixmap(pixmap)
        self.ui.mapPreview.setFixedSize(pixmap.size())
    
    def scale_reset(self):
    
        pixmap = QtGui.QPixmap(self.map_directory)
        pixmap = pixmap.scaledToHeight(self.map_height*6, False)
        self.ui.mapPreview.setPixmap(pixmap)
        self.ui.mapPreview.setFixedSize(pixmap.size())
        
    def add_toolbar(self, iconPath, name, function = None, shortcut = None):
        
        action = QtGui.QAction(QtGui.QIcon(iconPath), name, self)
        if shortcut:
            action.setShortcut(shortcut)
        self.toolbar = self.addToolBar(name)
        if function:
            action.triggered.connect(function)
        self.toolbar.addAction(action)
class EntityLabel (QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.minimumSize = (64,64)
        self.maximumSize = (64,64)
        self.setText ("Entity")
class MapPreview (QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
class ScrollAreaMap (QtGui.QScrollArea):
    def __init__(self, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
    def sizeHint(self):
        return QtCore.QSize(500,700)
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
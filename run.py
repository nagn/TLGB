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
    
    #Load Map, and grab the map data
    self.map_width, self.map_height, mapBackground = self.load_map(self.map_directory)
    #Scale the map to 6x
    self.ui.mappreview.setScaledContents(True)
    mapBackground = mapBackground.scaledToHeight(self.map_height*6,False)
    self.ui.mappreview.setPixmap(mapBackground)
    
    self.ui.mappreview.setFixedSize(mapBackground.size())
    
    #Bind the Corresponding Buttons/items into functions
    #Shrink Button
    QtCore.QObject.connect(self.ui.shrink, QtCore.SIGNAL("clicked()"), self.scale_down)
    #Enlarge Button
    QtCore.QObject.connect(self.ui.enlarge, QtCore.SIGNAL("clicked()"), self.scale_up)
    #Reset Button
    QtCore.QObject.connect(self.ui.reset, QtCore.SIGNAL("clicked()"), self.scale_reset)
    
  def load_map (self, map_directory):
    #We create a QImage in order to fetch map information
    img = QtGui.QImage(self.map_directory)

    #Convert the QImage into a QPixmap
    mapBackground = QtGui.QPixmap.fromImage(img)
    return (img.width(), img.height(), mapBackground)
  def scale_down(self):
    
    pixmap = QtGui.QPixmap(self.map_directory)
    pixmap = pixmap.scaledToHeight(self.map_height*3, False)
    self.ui.mappreview.setPixmap(pixmap)
    
  def scale_up(self):
    
    pixmap = QtGui.QPixmap(self.map_directory)
    pixmap = pixmap.scaledToHeight(self.map_height*9, False)
    self.ui.mappreview.setPixmap(pixmap)
    
  def scale_reset(self):
    
    pixmap = QtGui.QPixmap(self.map_directory)
    pixmap = pixmap.scaledToHeight(self.map_height*6, False)
    self.ui.mappreview.setPixmap(pixmap)

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
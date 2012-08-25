#!/usr/bin/env python
from __future__ import print_function, division
from PyQt4 import QtCore, QtGui
import settings as con
class MapWizard (QtGui.QWizard):
    def __init__(self, parent=None):
        super(MapWizard, self).__init__()
        self.setOption(QtGui.QWizard.NoDefaultButton, True)
        self.addPage(IntroPage())
        self.addPage(SettingsPage())
        self.setWindowTitle("Map Wizard")
        self.show()

class IntroPage (QtGui.QWizardPage):
    def __init__ (self, parent=None):
        super(IntroPage, self).__init__()
        self.setTitle("Introduction")
        label = QtGui.QLabel("This wizard will help you set up your map settings")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class SettingsPage (QtGui.QWizardPage):
    def __init__ (self, parent=None):
        super(SettingsPage, self).__init__()
        self.setTitle("Map Info")
        formLayout = SettingsForm()
        formLayout.addRow(("Name:"), QtGui.QLineEdit())
        formLayout.addRow(("Game Mode:"), QtGui.QLineEdit())
        self.wallmaskText = QtGui.QLineEdit()
        self.backgroundText = QtGui.QLineEdit()
        formLayout.addRow(("Wallmask:"),self.createFileBrowser(self.wallmaskText, self.openFileWallmask))
        formLayout.addRow(("Background:"),self.createFileBrowser(self.backgroundText, self.openFileBackground))
        formLayout.addRow(("Description:"), DescriptionBox())
        self.setLayout(formLayout)
        
        
    def openFileWallmask (self):
        con.WALLMASK_DIRECTORY = QtGui.QFileDialog.getOpenFileName()
        self.wallmaskText.setText(con.WALLMASK_DIRECTORY)
    def openFileBackground (self):
        con.BACKGROUND_DIRECTORY = QtGui.QFileDialog.getOpenFileName()
        self.backgroundText.setText(con.BACKGROUND_DIRECTORY)
    def createFileBrowser(self, lineEdit, openFile):
        #Initialize a row layout for the filebroweser + line edit
        horizontalLayout = QtGui.QHBoxLayout()
        
        browseButton = BrowseButton()
        browseButton.clicked.connect(openFile)
        
        horizontalLayout.addWidget(lineEdit)
        horizontalLayout.addWidget(browseButton)
        
        return(horizontalLayout)
class DescriptionBox (QtGui.QTextEdit):
    def __init__ (self, parent=None):
        super(DescriptionBox, self).__init__()
        self.setAlignment(QtCore.Qt.AlignTop)
    def sizeHint(self):
        return(QtCore.QSize(200,200))
class SettingsForm (QtGui.QFormLayout):
    def __init__ (self, parent=None):
        super(SettingsForm, self).__init__()
class BrowseButton (QtGui.QPushButton):
    def __init__ (self, parent=None):
        super(BrowseButton, self).__init__()
        self.setText("Browse")
        self.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
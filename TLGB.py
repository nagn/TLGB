# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GarrisonBuilder.ui'
#
# Created: Fri Aug 10 21:30:15 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapEditor(object):
    def setupUi(self, MapEditor):
        MapEditor.setObjectName(_fromUtf8("MapEditor"))
        MapEditor.resize(800, 600)
        MapEditor.setLayoutDirection(QtCore.Qt.LeftToRight)
        MapEditor.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(MapEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayoutEntity = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutEntity.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayoutEntity.setObjectName(_fromUtf8("verticalLayoutEntity"))
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        MapEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MapEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuMacros = QtGui.QMenu(self.menubar)
        self.menuMacros.setObjectName(_fromUtf8("menuMacros"))
        MapEditor.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MapEditor)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MapEditor.setStatusBar(self.statusBar)
        self.actionNew = QtGui.QAction(MapEditor)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MapEditor)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MapEditor)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(MapEditor)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionChange_Map_Type = QtGui.QAction(MapEditor)
        self.actionChange_Map_Type.setObjectName(_fromUtf8("actionChange_Map_Type"))
        self.actionSave_Entitites = QtGui.QAction(MapEditor)
        self.actionSave_Entitites.setObjectName(_fromUtf8("actionSave_Entitites"))
        self.actionSave_Maskdata = QtGui.QAction(MapEditor)
        self.actionSave_Maskdata.setObjectName(_fromUtf8("actionSave_Maskdata"))
        self.actionQuit = QtGui.QAction(MapEditor)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionDock_Widget = QtGui.QAction(MapEditor)
        self.actionDock_Widget.setObjectName(_fromUtf8("actionDock_Widget"))
        self.actionCopy = QtGui.QAction(MapEditor)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MapEditor)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionWallmask = QtGui.QAction(MapEditor)
        self.actionWallmask.setCheckable(True)
        self.actionWallmask.setChecked(True)
        self.actionWallmask.setObjectName(_fromUtf8("actionWallmask"))
        self.actionEntities = QtGui.QAction(MapEditor)
        self.actionEntities.setCheckable(True)
        self.actionEntities.setChecked(True)
        self.actionEntities.setObjectName(_fromUtf8("actionEntities"))
        self.actionMirror_Entities = QtGui.QAction(MapEditor)
        self.actionMirror_Entities.setObjectName(_fromUtf8("actionMirror_Entities"))
        self.actionTest = QtGui.QAction(MapEditor)
        self.actionTest.setCheckable(True)
        self.actionTest.setObjectName(_fromUtf8("actionTest"))
        self.actionBackground = QtGui.QAction(MapEditor)
        self.actionBackground.setCheckable(True)
        self.actionBackground.setChecked(True)
        self.actionBackground.setObjectName(_fromUtf8("actionBackground"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuView.addAction(self.actionBackground)
        self.menuView.addAction(self.actionWallmask)
        self.menuView.addAction(self.actionEntities)
        self.menuMacros.addAction(self.actionMirror_Entities)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuMacros.menuAction())

        self.retranslateUi(MapEditor)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), MapEditor.close)
        QtCore.QMetaObject.connectSlotsByName(MapEditor)

    def retranslateUi(self, MapEditor):
        MapEditor.setWindowTitle(QtGui.QApplication.translate("MapEditor", "Garrison Builder", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MapEditor", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MapEditor", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MapEditor", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMacros.setTitle(QtGui.QApplication.translate("MapEditor", "Macros", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MapEditor", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MapEditor", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MapEditor", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MapEditor", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChange_Map_Type.setText(QtGui.QApplication.translate("MapEditor", "Change Map Type", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Entitites.setText(QtGui.QApplication.translate("MapEditor", "Save Entitites", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Maskdata.setText(QtGui.QApplication.translate("MapEditor", "Save Maskdata", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MapEditor", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDock_Widget.setText(QtGui.QApplication.translate("MapEditor", "Dock Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MapEditor", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("MapEditor", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MapEditor", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("MapEditor", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWallmask.setText(QtGui.QApplication.translate("MapEditor", "Wallmask", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEntities.setText(QtGui.QApplication.translate("MapEditor", "Entities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMirror_Entities.setText(QtGui.QApplication.translate("MapEditor", "Mirror Entities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest.setText(QtGui.QApplication.translate("MapEditor", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBackground.setText(QtGui.QApplication.translate("MapEditor", "Background", None, QtGui.QApplication.UnicodeUTF8))


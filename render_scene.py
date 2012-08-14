#!/usr/bin/env python
from __future__ import print_function, division
from PyQt4 import QtCore, QtGui
class MapPreviewScene(QtGui.QGraphicsScene):
    def __init__(self, backgroundImage, wallmaskImage, renderingList, redundentLegacyList, form, parent=None):
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
        self.redundentLegacyList = redundentLegacyList
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
        
        redundantEntities =[item for item in self.items() if item.data(0) in self.redundentLegacyList
                            and item != self.wallmask and item != self.background]
        basicEntities = [item for item in self.items() if item.data(0) not in self.redundentLegacyList
                         and item != self.wallmask and item != self.background]
        
        for basicEntity in basicEntities:
            if self.form.basicEntitiesVisible:
                basicEntity.show()
            else:
                basicEntity.hide()
            basicEntity.update()
        for redundentEntity in redundantEntities:
            if self.form.redundentEntitiesVisible:
                redundentEntity.show()
            else:
                redundentEntity.hide()
            redundentEntity.update()
        
    def changeScale(self, scaleLevel):
        viewTransform = self.view.transform()
        viewTransform.reset()
        viewTransform = viewTransform.scale(scaleLevel,scaleLevel)
        self.view.setTransform(viewTransform)
class MapPreview(QtGui.QWidget):
    def __init__(self, background, wallmaskBackground, wallmaskBitmap, renderingList, form, parent=None):
        super(MapPreview, self).__init__(parent)
        #We need to do this to capture key input
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        #Pregenerate the different background states
        self.background = background
        self.wallmaskBitmap = wallmaskBitmap
        self.wallmaskBackground = wallmaskBackground.copy() 
        self.backgroundAndWallmask = self.background.copy()
        self.backgroundAndWallmask.setMask(self.wallmaskBitmap)
        
        self.x,self.y = (0,0)
        self.form = form
        self.hspeed = 0
        self.vspeed = 0
        self.friction = 0.35
        self.keyByteSequence = 0x0
        #self.setAutoFillBackground(True)
        
        #Set the transparent background to be pure black by default
        #palette = QtGui.QPalette()
        #palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        #self.setPalette(palette)
        
        self.renderingList = renderingList
    def sizeHint(self):
        return QtCore.QSize(500, 700)
    def minimumSizeHint(self):
        return QtCore.QSize(100, 100);
    #def paintEvent(self, event):
    #    
    #    qp = QtGui.QPainter()
    #    qp.begin(self)
    #    qp.setViewport(-self.x, -self.y, self.frameSize().width(), self.frameSize().height())
    #    qp.save()
    #    qp.scale(self.form.mapZoomLevel,self.form.mapZoomLevel)
    #    self.drawPixmaps(event, qp)
    #    qp.restore()
    #    #The entities are prescaled at 6x, so we compensate
    #    qp.scale(self.form.mapZoomLevel/6,self.form.mapZoomLevel/6)
    #    if self.form.entitiesVisible == True:
    #        self.drawEntities(event, qp)
    #    qp.end()
    ##    
    def drawEntities(self, event, qp):
        for iteration in range(len(self.renderingList)):
            x = self.renderingList[iteration][1][0]
            y = self.renderingList[iteration][1][1]
            qp.drawPixmap(QtCore.QPoint(x, y), self.renderingList[iteration][0])
    def drawPixmaps(self, event, qp):
        #Handle scrolling
        if self.keyByteSequence & 0x01:
            self.hspeed+=5
        if self.keyByteSequence & 0x02:
            self.hspeed-=5
        if self.keyByteSequence & 0x04:
            self.vspeed-=5
        if self.keyByteSequence & 0x08:
            self.vspeed+=5
        
        self.hspeed*=(1-self.friction)
        self.vspeed*=(1-self.friction)
        self.x += self.hspeed
        self.y += self.vspeed
        #compensate for top left coordinate system
        if self.x > self.background.width() * self.form.mapZoomLevel - self.frameSize().width():
            self.x = self.background.width()* self.form.mapZoomLevel - self.frameSize().width()
        elif self.x < 0:
            self.x = 0
        if self.y > self.background.height()* self.form.mapZoomLevel - self.frameSize().height():
            self.y = self.background.height()* self.form.mapZoomLevel - self.frameSize().height()
        elif self.y < 0:
            self.y = 0
        
        if abs(self.hspeed) < 0.02:
            self.hspeed = 0.0
        if abs(self.vspeed) < 0.02:
            self.vspeed = 0.0
                #target = event.rect()
        #translated doesn't modify the target in-place
        #source = target.translated(self.x, self.y)
        if self.form.wallmaskVisible and self.form.backgroundVisible:
            qp.drawPixmap(QtCore.QPoint(0, 0), self.backgroundAndWallmask)
        elif not self.form.wallmaskVisible and self.form.backgroundVisible:
            qp.drawPixmap(QtCore.QPoint(0, 0), self.background)
        elif self.form.wallmaskVisible and not self.form.backgroundVisible:
            qp.drawPixmap(QtCore.QPoint(0, 0),self.wallmaskBackground)
    def keyPressEvent(self, event):
        key_left = QtGui.QKeySequence.fromString("a")
        key_right = QtGui.QKeySequence.fromString("d")
        key_up = QtGui.QKeySequence.fromString("w")
        key_down = QtGui.QKeySequence.fromString("s")
        if event.isAutoRepeat()  == False:
            self.keyByteSequence = 0x0
            if event.key() == (key_right):
                self.keyByteSequence |= 0x01
                #+hspeed
                event.accept()
            if event.key() == (key_left):
                self.keyByteSequence |= 0x02
                #-hspeed
                event.accept()
            if event.key() == (key_up):
                self.keyByteSequence |= 0x04
                #self.vspeed-=1
                event.accept()
            if event.key() == (key_down):
                self.keyByteSequence |= 0x08
                #self.vspeed+=1
                event.accept()
    def keyReleaseEvent(self, event):
        key_left = QtGui.QKeySequence.fromString("a")
        key_right = QtGui.QKeySequence.fromString("d")
        key_up = QtGui.QKeySequence.fromString("w")
        key_down = QtGui.QKeySequence.fromString("s")
        if event.isAutoRepeat()  == False:
            if event.key() == (key_right):
                self.keyByteSequence &= 0xE
                event.accept()
            if event.key() == (key_left):
                self.keyByteSequence &= 0xD
                event.accept()
            if event.key() == (key_up):
                self.keyByteSequence &= 0xB
                event.accept()
            if event.key() == (key_down):
                self.keyByteSequence &= 0x7
                event.accept()
    def focusOutEvent(self, event):
        self.keyByteSequence = 0x0
#!/usr/bin/env python
from __future__ import print_function, division
from PyQt4 import QtCore, QtGui
from form.map_editor import MyForm
import sys
if __name__ == "__main__":
    
    app = QtGui.QApplication([""])
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
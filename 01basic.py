import sys
from OpenGL.GL import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

    def initializeGL(self):
        # Add OpenGL initialization code here
        pass

    def paintGL(self):
        # Update the scene here

        # Clear the screen
        glClearColor(1.0, 0.5, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the scene here

        # Tell the widget to redraw next time
        self.update()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = GLWidget()
    w.resize(512, 512)
    w.show()
    a.exec_()

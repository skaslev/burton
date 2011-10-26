import sys
from math import pi, sin, cos
from random import uniform, randrange
from OpenGL.GL import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from camera import MayaCamera

class Particle:
    def __init__(self, pos, vel, col):
        self.age = 0.0
        self.pos = pos
        self.vel = vel
        self.col = col

class ParticleSystem:
    def __init__(self):
        self.timer = QTime()
        self.timer.start()
        self.particles = []
        self.carry = 0

    def update(self):
        # Get elapsed time in seconds and reset the timer
        t = self.timer.elapsed() / 1000.0
        self.timer.start()

        # Update the particles
        for p in self.particles:
            p.age += t
            p.pos += t * p.vel
            p.vel += t * QVector3D(0, -0.2, 0)

        # Remove old particles
        self.particles = [p for p in self.particles if p.age < 10]

        # Spawn new particles
        n = 100 * t + self.carry
        nr_particles = int(n)
        self.carry = n - nr_particles
        for i in xrange(nr_particles):
            pos = QVector3D(0, 0, 0)
            phi = uniform(0, 2 * pi)
            theta = uniform(0, 0.5 * pi)
            vel = 0.7 * QVector3D(sin(theta) * cos(phi), cos(theta), sin(theta) * sin(phi))
            col = QVector3D(uniform(0, 1), uniform(0, 1), uniform(0, 1))
            self.particles.append(Particle(pos, vel, col))

    def draw(self):
        glPointSize(1.5)
        glBegin(GL_POINTS)
        for p in self.particles:
            glColor3f(p.col.x(), p.col.y(), p.col.z())
            glVertex3f(p.pos.x(), p.pos.y(), p.pos.z())
        glEnd()

def drawGradient():
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDepthMask(GL_FALSE)
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.1, 0.1)
    glVertex3f(-1, -1, 0)
    glVertex3f(1, -1, 0)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(1, 1, 0)
    glVertex3f(-1, 1, 0)
    glEnd()
    glPopAttrib()

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.camera = MayaCamera()
        self.psys = ParticleSystem()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POINT_SMOOTH)

    def paintGL(self):
        # Update the particle system
        self.psys.update()

        # Clear the screen
        glClear(GL_DEPTH_BUFFER_BIT)
        drawGradient()

        # Setup camera
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixf(self.camera.proj_matrix.data())
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.camera.view_matrix.data())

        # Draw the particle system
        self.psys.draw()

        # Tell the widget to redraw next time
        self.update()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.camera.aspect = float(width) / height

    def mousePressEvent(self, event):
        self.last_pos = event.posF()

    def mouseMoveEvent(self, event):
        dxy = event.posF() - self.last_pos
        dx = dxy.x() / self.width()
        dy = dxy.y() / self.height()
        if event.buttons() & Qt.LeftButton:
            self.camera.rotate(dx, dy)
        elif (event.buttons() & Qt.MidButton) or (event.modifiers() & Qt.ControlModifier):
            self.camera.pan(dx, dy)
        elif event.buttons() & Qt.RightButton:
            self.camera.zoom(dx, dy)
        self.last_pos = event.posF()

    def wheelEvent(self, event):
        self.camera.zoom(event.delta() / 360.0, 0.0)

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = GLWidget()
    w.resize(512, 512)
    w.show()
    a.exec_()

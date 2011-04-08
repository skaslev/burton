from math import tan, radians
from PyQt4.QtGui import QVector3D, QMatrix4x4

class MayaCamera:
    def __init__(self):
        self.center = QVector3D(0.0, 0.0, 0.0)
        self.focal_len = 5.0
        self.y_rot = 0.0
        self.x_rot = 0.0

        self.fovy  = 60.0
        self.aspect = 1.0
        self.znear = 0.1
        self.zfar = 1000.0

    def frame(self):
        x = QVector3D(1.0, 0.0, 0.0)
        y = QVector3D(0.0, 1.0, 0.0)
        z = QVector3D(0.0, 0.0, 1.0)

        m = QMatrix4x4()
        m.rotate(self.y_rot, y)
        x = m * x
        z = m * z

        m = QMatrix4x4()
        m.rotate(self.x_rot, x)
        y = m * y
        z = m * z

        return (x, y, z)

    @property
    def proj_matrix(self):
        res = QMatrix4x4()
        res.perspective(self.fovy, self.aspect, self.znear, self.zfar)
        return res

    @property
    def view_matrix(self):
        (x, y, z) = self.frame()
        res = QMatrix4x4()
        res.lookAt(self.center + self.focal_len * z, self.center, y)
        return res

    def rotate(self, dx, dy):
        self.y_rot -= dx * 360.0
        self.x_rot -= dy * 360.0

    def pan(self, dx, dy):
        ly = 2.0 * self.focal_len * tan(radians(self.fovy / 2.0))
        lx = ly * self.aspect
        (x, y, z) = self.frame()
        self.center -= dx * lx * x
        self.center += dy * ly * y

    def zoom(self, dx, dy):
        self.focal_len *= (1.0 - dy) - dx
        self.focal_len = max(self.focal_len, 0.1)

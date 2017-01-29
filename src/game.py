"""
Main game entry point
"""
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from math import cos, sin, radians

from car.car import Car


# pylint: disable = E1101
# Type guessing wrong
class Game(ShowBase):
    """
    The Class that starts the game
    """

    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        self.scene = self.loader.loadModel('models/track1')
        self.scene.reparentTo(self.render)
        self.scene.setScale(1.25, 1.25, 1.25)

        self.car = Car('models/car1',
                       pos=(0, 60, 1),
                       hpr=(90, 0, 0),
                       scale=(0.25, 0.25, 0.25),
                       showBase=self)

        self.car.reparentTo(self.render)

        self.taskMgr.add(self.alignCameraBehindCar, "Align Camera Behind Car")
        self.car.initialisePhysics()

    def alignCameraBehindCar(self, task):
        """
        Ensure that the player's view is behind the car.
        """
        carXpos, carYpos, carZpos = self.car.getPos()
        carHeadingDegrees, carPitchDegrees, carRollDegrees = self.car.getHpr()
        cameraHeadingDegrees = carHeadingDegrees
        cameraPitchDegrees = carPitchDegrees
        cameraRollDegrees = carRollDegrees

        carHeadingRadians = radians(carHeadingDegrees)

        cameraXpos = carXpos + 3.5 * sin(carHeadingRadians)
        cameraYpos = carYpos - 3.5 * cos(carHeadingRadians)
        self.camera.setPos(cameraXpos, cameraYpos, carZpos + 0.4)
        self.camera.setHpr(
            cameraHeadingDegrees, cameraPitchDegrees, cameraRollDegrees)
        return Task.cont

if __name__ == '__main__':
    game = Game()
    game.run()

"""
Main game entry point
"""
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from math import cos, sin, radians


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

        self.car = self.loader.loadModel('models/car1')
        self.car.setPos(0, 50, 1)
        self.car.setHpr(90, 0, 0)
        self.car.reparentTo(self.render)

        self.taskMgr.add(self.alignCameraBehindCar, "Align Camera Behind Car")

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

        cameraXpos = carXpos + 10 * sin(carHeadingRadians)
        cameraYpos = carYpos - 10 * cos(carHeadingRadians)
        self.camera.setPos(cameraXpos, cameraYpos, carZpos + 1)
        self.camera.setHpr(
            cameraHeadingDegrees, cameraPitchDegrees, cameraRollDegrees)
        return Task.cont

if __name__ == '__main__':
    game = Game()
    game.run()

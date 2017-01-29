"""
Main game entry point
"""
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

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
        self.enableParticles()

        self.scene = self.loader.loadModel('models/track1')
        self.scene.reparentTo(self.render)
        self.scene.setScale(1.25, 1.25, 1.25)

        self.car = Car('models/car1',
                       pos=(0, 60, 1),
                       hpr=(90, 0, 0),
                       scale=(0.25, 0.25, 0.25),
                       showBase=self)

        self.taskMgr.add(self.alignCameraBehindCar, "Align Camera Behind Car")

        self.camera.reparentTo(self.car.pandaNode)


        self.car.initialisePhysics()

    def alignCameraBehindCar(self, task):
        """
        Ensure that the player's view is behind the car.
        """
        self.camera.setPos(0, -10, 1.4)
        self.camera.setHpr(0, 0, 0)
        return Task.cont

if __name__ == '__main__':
    game = Game()
    game.run()

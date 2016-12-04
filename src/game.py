"""
Main game entry point
"""
from direct.showbase.ShowBase import ShowBase


class Game(ShowBase):
    """
    The Class that starts the game
    """

    def __init__(self):
        ShowBase.__init__(self)

#         self.disableMouse()
        self.scene = self.loader.loadModel('models/environment')
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.car = self.loader.loadModel('models/car1')
        self.car.setPos(0, 0, 1)
        self.car.reparentTo(self.render)

if __name__ == '__main__':
    game = Game()
    game.run()

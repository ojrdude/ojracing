"""
Car definition and physics.
"""
from direct.actor.Actor import Actor
from direct.task.Task import Task
from math import radians, sin, cos
from panda3d.core import KeyboardButton


class Car(Actor):
    """
    A car within the game
    """

    _ACCELERATION_RATE = 0.001
    _DECELERATION_RATE = 0.001
    _TURNING_RATE = 0.4
    _TOP_SPEED = 10

    def __init__(self, model, pos, hpr, scale, showBase):
        super(Car, self).__init__(models=model)
        self.setPos(pos)
        self.setHpr(hpr)
        self.setScale(scale)

        self._showBase = showBase
        self._speed = 0

    def initialisePhysics(self):
        """
        Sets up and starts the physics of the car.
        """
        self._showBase.taskMgr.add(self._acceleration, 'Calculate car acceleration')
        self._showBase.taskMgr.add(self._steer, 'Calculate car steering')
        self._showBase.taskMgr.add(self._move, 'Move Car')

    def _acceleration(self, task):
        """
        Check if the accelerator key is being pressed and increase
        the car's speed if it is. Currently the accelerator is UP.
        """
        isDown = self._showBase.mouseWatcherNode.is_button_down

        if isDown(KeyboardButton.up()):
            speedIncrease = task.time * self._ACCELERATION_RATE
            newSpeed = self._speed + speedIncrease
            if newSpeed > self._TOP_SPEED:
                self._speed = self._TOP_SPEED
            else:
                self._speed = newSpeed
        else:
            speedDecrease = task.time * self._DECELERATION_RATE
            newSpeed = self._speed - speedDecrease
            if newSpeed < 0:
                self._speed = 0
            else:
                self._speed = newSpeed

        return Task.cont

    def _move(self, task):
        """
        Move the car in the direction it is facing. How far it is moved
        is dependent on its speed.
        """
        currentX, currentY, currentZ = self.getPos()
        currentHeadingDegrees, _, _ = self.getHpr()

        currentHeadingRadians = radians(currentHeadingDegrees)

        newXPos = currentX - self._speed * sin(currentHeadingRadians) * task.time
        newYPos = currentY + self._speed * cos(currentHeadingRadians) * task.time

        self.setPos(newXPos, newYPos, currentZ)

        return Task.cont

    def _steer(self, task):
        """
        Change the heading of the car if the steer left or steer right button
        is pressed.
        """
        isDown = self._showBase.mouseWatcherNode.is_button_down

        leftPressed = isDown(KeyboardButton.left())
        rightPressed = isDown(KeyboardButton.right())
        if leftPressed == rightPressed:
            # Both pressed or neither pressed
            return Task.cont

        currentHeading = self.getH()

        if leftPressed:
            self.setH(currentHeading + task.time * self._TURNING_RATE)
        else:
            self.setH(currentHeading - task.time * self._TURNING_RATE)

        return Task.cont

"""
Car definition and physics.
"""
from direct.task.Task import Task
from panda3d.core import KeyboardButton, NodePath
from panda3d.physics import ActorNode, ForceNode, LinearVectorForce


class Car(object):
    """
    A car within the game
    """

    _MASS = 1000  # kg
    _ACCEL = 100
    _ENGINE_BRAKING = 80
    _TOP_SPEED = 100

    def __init__(self, model, pos, hpr, scale, showBase):
        self.node = NodePath('CarPhysicsNode')
        self.node.reparentTo(showBase.render)
        self.node.setPos(pos)
        self.node.setHpr(hpr)
        self.node.setScale(scale)

        self.actorNode = ActorNode('CarPhysics')
        self.pandaNode = self.node.attachNewNode(self.actorNode)
        showBase.physicsMgr.attachPhysicalNode(self.actorNode)
        self.model = showBase.loader.loadModel(model)
        self.model.reparentTo(self.pandaNode)

        self._showBase = showBase
        self.actorNode.getPhysicsObject().setMass(self._MASS)

        self._accelForce, self._deccelForce = self._initialiseAccelAndDeccel()


    def initialisePhysics(self):
        """
        Sets up and starts the physics of the car.
        """
        self._showBase.taskMgr.add(self._accelerate, 'acceleration')

    def _accelerate(self, task):
        """
        Perform acceleration by applying acceleration force or engine
        braking depending on whether the accelerator is being pressed.
        """
        isDown = self._showBase.mouseWatcherNode.is_button_down
        physicalObject = self.actorNode.getPhysical(0)
        if isDown(KeyboardButton.up()):
            physicalObject.addLinearForce(self._accelForce)
            physicalObject.removeLinearForce(self._deccelForce)
            return Task.cont

        _, speed, _ = self.actorNode.getPhysicsObject().getVelocity()
        if speed <= 0:
            physicalObject.removeLinearForce(self._deccelForce)
        elif speed >= self._TOP_SPEED:
            physicalObject.removeLinearForce(self._accelForce)
        else:
            physicalObject.addLinearForce(self._deccelForce)
            physicalObject.removeLinearForce(self._accelForce)

        return Task.cont

    def _initialiseAccelAndDeccel(self):
        """
        Define and return the acceleration and engine braking forces
        """
        accelFN = ForceNode('acceleration')
        deccelFN = ForceNode('deceleration')
        self.node.attachNewNode(accelFN)
        self.node.attachNewNode(deccelFN)

        accelForce = LinearVectorForce(0, self._ACCEL, 0)
        accelForce.setMassDependent(1)
        deccelForce = LinearVectorForce(0, -1 * self._ENGINE_BRAKING, 0)
        deccelForce.setMassDependent(1)
        accelFN.addForce(accelForce)
        deccelFN.addForce(deccelForce)

        return accelForce, deccelForce

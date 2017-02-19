"""
Car definition and physics.
"""
from direct.task.Task import Task
from panda3d.core import KeyboardButton, NodePath
from panda3d.physics import ActorNode, ForceNode, LinearVectorForce, \
    AngularVectorForce, AngularEulerIntegrator


class Car(object):
    """
    A car within the game
    """

    _MASS = 1000  # kg
    _ACCEL = 10000  # N
    _ENGINE_BRAKING = 8000  # N
    _TOP_SPEED = 100
    _STEERING_TORQUE = 0.1  # Nm

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
        self._leftRotForce, self._rightRotForce = self._initialiseTurningForces()


    def initialisePhysics(self):
        """
        Sets up and starts the physics of the car.
        """
        self._showBase.taskMgr.add(self._accelerate, 'acceleration')
        self._showBase.taskMgr.add(self._steering, 'steering')
        self._showBase.physicsMgr.attachAngularIntegrator(AngularEulerIntegrator())

    # pylint: disable=W0613
    # task needed for Task interface but not actually used.
    def _accelerate(self, task):
        """
        Perform acceleration by applying acceleration force or engine
        braking depending on whether the accelerator is being pressed.
        """
        isDown = self._showBase.mouseWatcherNode.is_button_down
        physicalObject = self.actorNode.getPhysical(0)
        currentForceList = physicalObject.getLinearForces()
        if isDown(KeyboardButton.up()):
            if self._accelForce not in currentForceList:
                physicalObject.addLinearForce(self._accelForce)
            physicalObject.removeLinearForce(self._deccelForce)
            return Task.cont

        _, speed, _ = self.actorNode.getPhysicsObject().getVelocity()
        if speed <= 0:
            physicalObject.removeLinearForce(self._deccelForce)
        elif speed >= self._TOP_SPEED:
            physicalObject.removeLinearForce(self._accelForce)
        else:
            if self._deccelForce not in currentForceList:
                physicalObject.addLinearForce(self._deccelForce)
            physicalObject.removeLinearForce(self._accelForce)

        return Task.cont
    # pylint: enable=W0613

    # pylint: disable=W0613
    # task needed for Task interface but not actually used.
    def _steering(self, task):
        """
        Perform steering by applying rotational forces to the car depending
        on whether the left or right key is pressed.
        """
        isDown = self._showBase.mouseWatcherNode.is_button_down
        physicalObject = self.actorNode.getPhysical(0)
        currentForceList = physicalObject.getAngularForces()
        if isDown(KeyboardButton.left()) == isDown(KeyboardButton.right()):
            # Both down or neither should be treated as no steering.
            physicalObject.removeAngularForce(self._leftRotForce)
            physicalObject.removeAngularForce(self._rightRotForce)
            return Task.cont

        if isDown(KeyboardButton.left()):
            if self._leftRotForce not in currentForceList:
                physicalObject.addAngularForce(self._leftRotForce)
            physicalObject.removeAngularForce(self._rightRotForce)
        else:
            if self._rightRotForce not in currentForceList:
                physicalObject.addAngularForce(self._rightRotForce)
            physicalObject.removeAngularForce(self._leftRotForce)
        return Task.cont
    # pylint: enable=W0613

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

    def _initialiseTurningForces(self):
        """
        Define and return the turning forces for steering.
        """
        leftRotFN = ForceNode('leftRotation')
        rightRotFN = ForceNode('rightRotation')
        self.node.attachNewNode(leftRotFN)
        self.node.attachNewNode(rightRotFN)

        leftRotForce = AngularVectorForce(self._STEERING_TORQUE, 0, 0)
        rightRotForce = AngularVectorForce(-1 * self._STEERING_TORQUE, 0, 0)
        leftRotFN.addForce(leftRotForce)
        rightRotFN.addForce(rightRotForce)

        return leftRotForce, rightRotForce

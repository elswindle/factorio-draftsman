# mining_drill.py

from draftsman.prototypes.mixins import (
    RequestItemsMixin, CircuitReadResourceMixin, CircuitConditionMixin,
    EnableDisableMixin, LogisticConditionMixin, ControlBehaviorMixin,
    CircuitConnectableMixin, DirectionalMixin, Entity
)
from draftsman.errors import InvalidEntityID
from draftsman.utils import warn_user

from draftsman.data.entities import mining_drills


class MiningDrill(RequestItemsMixin, CircuitReadResourceMixin, 
                  CircuitConditionMixin, EnableDisableMixin, 
                  LogisticConditionMixin, ControlBehaviorMixin, 
                  CircuitConnectableMixin, DirectionalMixin, Entity):
    def __init__(self, name: str = mining_drills[0], **kwargs):
        if name not in mining_drills:
            raise InvalidEntityID("'{}' is not a valid name for this type"
                                  .format(name))
        super(MiningDrill, self).__init__(name, **kwargs)

        for unused_arg in self.unused_args:
            warn_user("{} has no attribute '{}'".format(type(self), unused_arg))
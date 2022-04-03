# directional.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman import signatures
from draftsman.constants import Direction
from draftsman.error import DraftsmanError
from draftsman.warning import DirectionWarning

from schema import SchemaError
from typing import Union
import warnings


class DirectionalMixin(object):
    """
    Enables entities to be rotated.
    """

    def __init__(self, name, similar_entities, tile_position=[0, 0], **kwargs):
        # type: (str, list[str], Union[list, dict], **dict) -> None
        super(DirectionalMixin, self).__init__(name, similar_entities, **kwargs)

        self._rotatable = True

        # Keep track of the entities width and height regardless of rotation
        self.static_tile_width = self.tile_width
        self.static_tile_height = self.tile_height
        self.static_collision_box = self.collision_box

        self.direction = 0
        if "direction" in kwargs:
            self.direction = kwargs["direction"]
            self.unused_args.pop("direction")
        self._add_export("direction", lambda x: x != 0)

        # Technically redundant, but we reset the position if the direction has
        # changed to reflect its changes
        if "position" in kwargs:
            self.position = kwargs["position"]
        else:
            self.tile_position = tile_position

    # =========================================================================

    @property
    def direction(self):
        # type: () -> Direction
        """
        TODO
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        # type: (Direction) -> None
        if self.blueprint:
            raise DraftsmanError(
                "Cannot set direction of entity while it's in a Blueprint"
            )

        if value is None:
            self._direction = Direction(0)  # Default Direction
        else:
            self._direction = Direction(value)

        if self._direction not in {0, 2, 4, 6}:
            warnings.warn(
                "'{}' only has 4-way rotation".format(type(self).__name__),
                DirectionWarning,
                stacklevel=2,
            )
        if self._direction == Direction.EAST or self._direction == Direction.WEST:
            self._tile_width = self.static_tile_height
            self._tile_height = self.static_tile_width
            self._collision_box[0] = [
                self.static_collision_box[0][1],
                self.static_collision_box[0][0],
            ]
            self._collision_box[1] = [
                self.static_collision_box[1][1],
                self.static_collision_box[1][0],
            ]
        else:
            self._tile_width = self.static_tile_width
            self._tile_height = self.static_tile_height
            self._collision_box = self.static_collision_box

        # Reset the grid/absolute positions in case the direction changed
        self.tile_position = (self.tile_position["x"], self.tile_position["y"])
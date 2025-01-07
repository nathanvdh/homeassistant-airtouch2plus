"""AirTouch 2+ zone entity."""

import logging
from typing import Any, final

from airtouch2.at2plus import At2PlusGroup

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@final
class AirTouch2PlusGroupEntity(FanEntity):
    """Representation of an AirTouch 2+ zone."""

    def __init__(self, group: At2PlusGroup) -> None:
        """Initialize the fan entity."""
        self._group = group

    #
    # Entity attributes:
    #
    _attr_should_poll: bool = False

    #
    # Entity overrides:
    #

    @property
    def unique_id(self) -> str:
        """Return unique ID for this device."""
        return f"at2plus_group_{self._group.status.id}"

    @property
    def name(self):
        """Return the name of this group."""
        return (
            self._group.name
            if self._group.name is not None
            else f"Group {self._group.status.id}"
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=self.name,
            manufacturer="Polyaire",
            model="Airtouch 2+",
        )

    async def async_added_to_hass(self) -> None:
        """Call when entity is added."""
        # Add callback for when group receives new data.
        # Removes callback on remove.
        self.async_on_remove(self._group.add_callback(self.async_write_ha_state))

    #
    # FanEntity overrides
    #

    @property
    def is_on(self):
        """Return if group is on."""
        return self._group.is_on()

    @property
    def percentage(self) -> int:
        """Return current percentage of the group damper."""
        return self._group.status.damp

    @property
    def supported_features(self) -> FanEntityFeature:
        """Fan supported features."""
        return (
            FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
            | FanEntityFeature.SET_SPEED
        )

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the group."""
        await self._group.turn_on(percentage)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the group."""
        await self._group.turn_off()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the group damper."""
        await self._group.set_damp(percentage)

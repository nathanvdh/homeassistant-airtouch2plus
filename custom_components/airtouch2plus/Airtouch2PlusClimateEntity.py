from airtouch2.at2plus import At2PlusAircon, AcMode

from .conversions import (
    AT2PLUS_TO_HA_MODE,
    AT2PLUS_SETMODE_TO_HA_MODE,
    AT2PLUS_TO_HA_FAN_SPEED,
    HA_MODE_TO_AT2PLUS_SETMODE,
    HA_FAN_SPEED_TO_AT2PLUS
)
from .const import DOMAIN

from typing import final

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    UnitOfTemperature,
    ATTR_TEMPERATURE,
    PRECISION_TENTHS
)
from homeassistant.helpers.entity import DeviceInfo


@final
class Airtouch2PlusClimateEntity(ClimateEntity):
    """Representation of an AirTouch 2+ AC."""

    #
    # Entity attributes:
    #
    _attr_should_poll: bool = False

    #
    # ClimateEntity attributes:
    #
    _attr_precision: float = PRECISION_TENTHS
    _attr_target_temperature_step: float = 0.1
    _attr_temperature_unit: str = UnitOfTemperature.CELSIUS

    def __init__(self, at2plus_aircon: At2PlusAircon) -> None:
        """Initialize the climate device."""
        self._ac = at2plus_aircon

    #
    # Entity overrides:
    #

    @property
    def unique_id(self) -> str:
        """Return unique ID for this device."""
        return f"at2plus_ac_{self._ac.status.id}"

    @property
    def name(self):
        """Return the name of the climate device."""
        if self._ac.ability is not None:
            return f"AC {self._ac.ability.name}"
        else:
            return self.unique_id

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
        # Add callback for when aircon receives new data
        # Removes callback on remove
        self.async_on_remove(self._ac.add_callback(self.async_write_ha_state))

    #
    # ClimateEntity overrides:
    #

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        if not self._ac.is_on():
            return HVACMode.OFF

        return AT2PLUS_TO_HA_MODE[self._ac.status.mode]

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available hvac operation modes."""
        modes: list[HVACMode] = [HVACMode.OFF]
        if self._ac.ability is not None:
            for mode in self._ac.ability.supported_modes:
                modes.append(AT2PLUS_SETMODE_TO_HA_MODE[mode])
        return modes

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        if self._ac.status.temperature is not None:
            return self._ac.status.temperature
        else:
            return 0

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        if self._ac.status.set_point is not None:
            return self._ac.status.set_point
        else:
            return 0

    @property
    def fan_mode(self) -> str:
        """Return fan mode of this AC."""
        return AT2PLUS_TO_HA_FAN_SPEED[self._ac.status.fan_speed]

    @property
    def fan_modes(self) -> list[str]:
        """Return the list of available fan modes."""
        if self._ac.ability is not None:
            return [AT2PLUS_TO_HA_FAN_SPEED[s] for s in self._ac.ability.supported_fan_speeds]
        return []

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        temp = float(kwargs.get(ATTR_TEMPERATURE, 0))
        await self._ac.set_setpoint(temp)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        await self._ac.set_fan_speed(HA_FAN_SPEED_TO_AT2PLUS[fan_mode])

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.OFF:
            if self._ac.is_on():
                await self.async_turn_off()
        else:
            if not self._ac.is_on():
                await self.async_turn_on()
            await self._ac.set_mode(HA_MODE_TO_AT2PLUS_SETMODE[hvac_mode])

    async def async_turn_on(self):
        """Turn on."""
        await self._ac.turn_on()

    async def async_turn_off(self):
        """Turn off."""
        await self._ac.turn_off()

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return the list of supported features."""
        # TODO: Verify this with someone with the system.
        mode: AcMode = self._ac.status.mode

        if mode == AcMode.DRY:
            # only because there's no ClimateEntityFeature.NONE
            return ClimateEntityFeature.TARGET_TEMPERATURE

        if mode == AcMode.FAN:
            return ClimateEntityFeature.FAN_MODE

        return ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE

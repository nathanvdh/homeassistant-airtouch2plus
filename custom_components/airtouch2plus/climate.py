"""AirTouch 2 component to control AirTouch 2 Climate Device."""
from __future__ import annotations

from airtouch2.at2plus import At2PlusClient
from .Airtouch2PlusClimateEntity import Airtouch2PlusClimateEntity
from .const import DOMAIN

import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Airtouch 2+."""
    airtouch2_client: At2PlusClient = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[ClimateEntity] = [
        Airtouch2PlusClimateEntity(ac) for ac in airtouch2_client.aircons_by_id.values()
    ]

    _LOGGER.debug(f" Found entities {[repr(entity) for entity in entities]}")
    async_add_entities(entities)

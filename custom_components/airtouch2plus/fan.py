from __future__ import annotations
import logging

from airtouch2.at2plus import At2PlusClient
from .Airtouch2PlusGroupEntity import AirTouch2PlusGroupEntity
from .const import DOMAIN

from homeassistant.components.fan import FanEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the AirTouch 2+ group entities."""
    client: At2PlusClient = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[FanEntity] = [
        AirTouch2PlusGroupEntity(group) for group in client.groups_by_id.values()
    ]

    if entities:
        async_add_entities(entities)

"""The airtouch2 integration."""

from typing import Any

from airtouch2.at2plus import At2PlusClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.FAN]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up airtouch2 from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    client = At2PlusClient(entry.data[CONF_HOST])
    if not await client.connect():
        raise ConfigEntryNotReady(
            f"Airtouch2+ client failed to connect to {entry.data[CONF_HOST]}"
        )
    client.run()
    await client.wait_for_ac()
    if not client.aircons_by_id:
        raise ConfigEntryNotReady("No AC units were found")
    hass.data[DOMAIN][entry.entry_id] = client
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        client: At2PlusClient = hass.data[DOMAIN][entry.entry_id]
        await client.stop()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Prefix pre-0.3 unique IDs with the config entry ID."""
    if entry.version == 1:
        prefix = f"at2plus_{entry.entry_id}_"

        def new_id(old: str) -> str | None:
            if old.startswith("at2plus_") and not old.startswith(prefix):
                return prefix + old.removeprefix("at2plus_")
            return None

        @callback
        def _migrate_unique_id(reg_entry: er.RegistryEntry) -> dict[str, Any] | None:
            if (uid := new_id(reg_entry.unique_id)) is not None:
                return {"new_unique_id": uid}
            return None

        # Migrate entity unique IDs.
        await er.async_migrate_entries(hass, entry.entry_id, _migrate_unique_id)

        # Migrate device identifiers (which contain the unique ID).
        dev_reg = dr.async_get(hass)
        for device in dr.async_entries_for_config_entry(dev_reg, entry.entry_id):
            ids = {
                (domain, new_id(ident) or ident)
                if domain == DOMAIN
                else (domain, ident)
                for domain, ident in device.identifiers
            }
            if ids != device.identifiers:
                dev_reg.async_update_device(device.id, new_identifiers=ids)

        hass.config_entries.async_update_entry(entry, version=2)

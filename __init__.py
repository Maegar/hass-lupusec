"""The lupusecxt integration."""
import asyncio
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from homeassistant.components.hass_lupusec.lupusecio import LupusecSystem

_LOGGER = logging.getLogger(__name__)

NOTIFICATION_ID = "lupusecxt_notification"
NOTIFICATION_TITLE = "Lupusec Security Setup"



CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.deprecated(CONF_NAME, invalidation_version="0.110"),
            vol.Schema({vol.Optional(CONF_NAME, default=DOMAIN): cv.string}),
        )
    },
    extra=vol.ALLOW_EXTRA,
)


PLATFORMS = ["alarm_control_panel", "switch"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the lupusecxt component."""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up lupusecxt from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = LupusecSystem(
        entry.data["username"], entry.data["password"], entry.data["host"], entry.data["ssl_verify"]
    )

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class LupusecDevice(Entity):
    """Representation of a Lupusec device."""

    def __init__(self, data, device, area):
        """Initialize a sensor for Lupusec device."""
        self._data = data
        self._device = device
        self._area = area

    @property
    def should_poll(self):
        """Return the name of the switch."""
        return False

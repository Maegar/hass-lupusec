"""Support for Lupusec Security System binary sensors."""
import asyncio
from datetime import timedelta
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.helpers.config_validation import (  # noqa: F401
    PLATFORM_SCHEMA,
    PLATFORM_SCHEMA_BASE,
)

from . import DOMAIN as LUPUSEC_DOMAIN

SCAN_INTERVAL = timedelta(days=100)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[LUPUSEC_DOMAIN][config_entry.entry_id]
    async_add_entities([TCPListener(hass, "cid-listener", 1081, STATE_OFF)])


class TCPListener(SwitchEntity):
    def __init__(self, hass, name, port, state):
        self._hass = hass
        self._name = name
        self._state = state
        self._port = port
        self._server = None
        self.async_on_remove(self.stop)

    @property
    def should_poll(self):
        """Return the name of the switch."""
        return False

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return "cid_listener"

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state == STATE_ON

    async def async_turn_on(self, **kwargs):
        _LOGGER.debug("async_turn_on %s:%d", self.name, self._port)
        self._state = STATE_ON
        await self.async_listen()

    async def async_turn_off(self, **kwargs):
        _LOGGER.debug("async_turn_off %s:%d", self.name, self._port)
        self.stop()

    def stop(self):
        self._state = STATE_OFF
        if self._server:
            self._server.close()
            self._server = None

    async def handle_connection(self, reader, writer):
        address = writer.get_extra_info("peername")
        writer.close()

    async def async_loop(self, server):
        async with server:
            await server.serve_forever()

    async def async_listen(self):
        _LOGGER.debug("async_listen %s:%d", self.name, self._port)
        server = await asyncio.start_server(self.handle_connection, None, self._port)
        _LOGGER.debug(
            "async_listen %s:%d on %s",
            self.name,
            self._port,
            server.sockets[0].getsockname(),
        )
        self._server = server
        self._hass.async_create_task(self.async_loop(server))
        _LOGGER.debug("async_listen done %s:%d", self.name, self._port)

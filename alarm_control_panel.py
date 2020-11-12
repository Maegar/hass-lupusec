"""Support for Lupusec System alarm control panels."""
from datetime import timedelta
import logging

import homeassistant.components.hass_lupusec.lupusecio.devices

from homeassistant.components.alarm_control_panel import (
    ALARM_SERVICE_SCHEMA,
    DOMAIN,
    ENTITY_ID_FORMAT,
    AlarmControlPanelEntity,
)
from homeassistant.components.alarm_control_panel.const import (
    SUPPORT_ALARM_ARM_AWAY,
    SUPPORT_ALARM_ARM_CUSTOM_BYPASS,
    SUPPORT_ALARM_ARM_HOME,
    SUPPORT_ALARM_ARM_NIGHT,
)
from homeassistant.components.switch import SwitchDevice
from homeassistant.const import (
    CONF_NAME,
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_CUSTOM_BYPASS,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
    STATE_ALARM_DISARMED,
    STATE_ALARM_TRIGGERED,
)
from homeassistant.helpers import config_entry_flow
from homeassistant.helpers.entity import Entity

from . import DOMAIN, LupusecDevice
from homeassistant.components.hass_lupusec.lupusecio.devices.AlarmPanel import AlarmPanel

ICON = "mdi:security"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """ hahah """
    name = config_entry.data.get(CONF_NAME) or DOMAIN
    lupusec_system = hass.data[DOMAIN][config_entry.entry_id]

    panel = AlarmPanel(lupusec_system)
    hass.data[DOMAIN]["supported_features"] = (
        SUPPORT_ALARM_ARM_AWAY
        | SUPPORT_ALARM_ARM_HOME
        | SUPPORT_ALARM_ARM_CUSTOM_BYPASS
        | SUPPORT_ALARM_ARM_NIGHT
    )

    await hass.async_add_executor_job(panel.do_update)
    hass.data[DOMAIN]["panel"] = panel
    hass.data[DOMAIN]["areas"] = []

    for area in panel.areas:
        hass.data[DOMAIN]["areas"].append(LupusecAlarm(lupusec_system, panel, area))

    async_add_entities(hass.data[DOMAIN]["areas"])

    hass.components.webhook.async_register(
        DOMAIN, "LupusecXT", "lupupdate", handle_webhook
    )


async def async_unload_entry(hass, entry):
    hass.components.webhook.async_unregister("lupupdate")


async def handle_webhook(hass, webhook_id, request):
    """Handle webhook callback."""
    await hass.async_add_executor_job(hass.data[DOMAIN]["panel"].do_update)
    for area in hass.data[DOMAIN]["areas"]:
        await area.async_update_ha_state(True)


# pylint: disable=invalid-name
async_remove_entry = config_entry_flow.webhook_async_remove_entry


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop("areas")
    return True


class LupusecAlarm(LupusecDevice, AlarmControlPanelEntity):
    """An alarm_control_panel implementation for Lupusec."""

    @property
    def icon(self):
        """Return the icon."""
        return ICON

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        if self._area.areaNo is None:
            return "area"
        else:
            return "area%d" % (self._area.areaNo)

    @property
    def state(self):
        """Return the state of the device."""
        if self._area.is_arm():
            state = STATE_ALARM_ARMED_AWAY
        elif self._area.is_disarm():
            state = STATE_ALARM_DISARMED
        elif self._area.is_home():
            state = STATE_ALARM_ARMED_HOME
        elif self._area.is_triggered():
            state = STATE_ALARM_TRIGGERED
        elif self._area.is_night():
            state = STATE_ALARM_ARMED_NIGHT
        elif self._area.is_custom_bypass():
            state = STATE_ALARM_ARMED_CUSTOM_BYPASS
        else:
            state = None
        return state

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return self.hass.data[DOMAIN]["supported_features"]

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return "lupusecxt__area"

    def alarm_arm_away(self, code=None):
        """Send arm away command."""
        self._area.set_arm()

    def alarm_disarm(self, code=None):
        """Send disarm command."""
        self._area.set_disarm()

    def alarm_arm_home(self, code=None):
        """Send arm home command."""
        self._area.set_home()

    def alarm_arm_custom_bypass(self, code=None):
        """Send custom by pass command."""
        self._area.set_custom_bypass()

    def alarm_arm_night(self, code=None):
        """Send custom by pass command."""
        self._area.set_night()

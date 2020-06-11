"""Config flow for Lupusec XTX integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)


DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): vol.All(str, vol.Length(min=1)),
        vol.Required("username"): vol.All(str, vol.Length(min=1)),
        vol.Required("password"): vol.All(str, vol.Length(min=1)),
        vol.Required("devicetype"): vol.All(str, vol.Length(min=3)),
    }
)


class LupusecHub:
    """LupusecHub - Main class for Integration configuration
    """

    def __init__(self, host, devicetype):
        """Initialize."""
        self.host = host
        self.devicetype = devicetype

    async def authenticate(self, username, password) -> bool:
        """Test if we can authenticate with the host."""
        # TODO LIB TEST
        return True


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    data["devicetype"] = data["devicetype"].strip()
    data["devicetype"] = data["devicetype"].lower()

    # TODO May adjust minimun length of fields or add regex check
    if (
        len(data["host"]) < 1
        or len(data["username"]) < 1
        or len(data["password"]) < 1
        or len(data["devicetype"]) < 3
    ):
        raise InvalidAuth

    if data["devicetype"] != "xt1" and data["devicetype"] != "xt2":
        raise InvalidAuth

    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    hub = LupusecHub(data["host"], data["devicetype"])

    if not await hub.authenticate(data["username"], data["password"]):
        raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    device_name = "Lupusec {} {}".format(data["devicetype"].upper(), data["host"])
    device_unique_id = "lupusec_{}_{}".format(data["devicetype"].lower(), data["host"])
    # Return info that you want to store in the config entry.
    return {"device_name": device_name, "device_unique_id": device_unique_id}


class LupusecXTXConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lupusec XTX."""

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    # TODO Not sure if PUSH or POLL, depends on LIB
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                await self.async_set_unique_id(info["device_unique_id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["device_name"], data=user_input
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""

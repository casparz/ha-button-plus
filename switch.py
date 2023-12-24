""" Platform for switch integration. """
from __future__ import annotations

import logging

from homeassistant.components.switch import (SwitchEntity, SwitchDeviceClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ButtonPlusHub

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

switches = []


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed config_entry in HA."""

    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]
    buttons = hub.config.mqtt_buttons

    for button in buttons:
        _LOGGER.debug(f"Creating switch with parameters: {button.button_id} {button.label} {hub.hub_id}")
        switches.append(ButtonPlusSwitch(button.button_id, hub.hub_id))

    async_add_entities(switches)


class ButtonPlusSwitch(SwitchEntity):
    def __init__(self, btn_id, hub_id):
        self._is_on = False
        self._attr_unique_id = f'switch-{hub_id}-{btn_id}'
        self._hub_id = hub_id
        self.entity_id = f"switch.{hub_id}_{btn_id}"
        self._attr_name = f'switch-{btn_id}'
        self._name = f'Button {btn_id}'
        self._device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._hub_id)}}

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False

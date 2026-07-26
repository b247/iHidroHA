# Copyright (C) 2026 b247_eu, https://b247.eu.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://opensource.org/license/gpl-3.0/>.
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import selector
from .const import DOMAIN, CONF_USER, CONF_PASS, CONF_UAN

class IHidroConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Set entry title as the UAN
            return self.async_create_entry(title=f"iHidro ({user_input[CONF_UAN]})", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_USER): str,
            vol.Required(CONF_PASS): selector({"text": {"type": "password"}}),
            vol.Required(CONF_UAN): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema)
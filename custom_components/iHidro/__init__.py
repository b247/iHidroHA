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
import os
import json
import platform
import urllib.request
import asyncio
import logging

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN, CONF_USER, CONF_PASS, CONF_UAN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # 1. Download/Verify the iHidro-cli Binary
    bin_dir = hass.config.path("custom_components", DOMAIN, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    binary_path = os.path.join(bin_dir, "iHidro-cli")

    if not os.path.exists(binary_path):
        arch = "amd64" if platform.machine() in ["x86_64", "AMD64"] else "arm64"
        url = f"https://github.com/b247/iHidroGo/releases/latest/download/ihidro-cli-linux-{arch}"

        def _download():
            _LOGGER.info("Downloading iHidro-cli binary from %s", url)
            urllib.request.urlretrieve(url, binary_path)
            os.chmod(binary_path, 0o755)

        await hass.async_add_executor_job(_download)

    # 2. Define Command Runner
    async def run_cli(command_flags: list) -> str:
        auth_data = json.dumps({
            "user": entry.data[CONF_USER],
            "pass": entry.data[CONF_PASS],
            "uan": entry.data[CONF_UAN],
        })
        args = [binary_path, "-authConfig", auth_data] + command_flags

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        out_str = stdout.decode().strip()
        err_str = stderr.decode().strip()

        if proc.returncode != 0:
            _LOGGER.error("iHidro CLI failed: %s", err_str)
            raise HomeAssistantError(f"iHidro CLI error: {err_str}")

        return out_str

    # 3. Register HA Services/Actions
    async def handle_submit_index(call: ServiceCall) -> dict:
        meter_value = str(call.data.get("value"))
        output = await run_cli(["-submitIndex", meter_value])
        return {"success": True, "output": output}

    async def handle_get_index_history(call: ServiceCall) -> dict:
        output = await run_cli(["-getIndexHistory"])
        try:
            return {"history": json.loads(output)}
        except json.JSONDecodeError:
            return {"output": output}

    hass.services.async_register(
        DOMAIN,
        "submit_index",
        handle_submit_index,
        supports_response=SupportsResponse.OPTIONAL,
    )
    hass.services.async_register(
        DOMAIN,
        "get_index_history",
        handle_get_index_history,
        supports_response=SupportsResponse.OPTIONAL,
    )

    return True
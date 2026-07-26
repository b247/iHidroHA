# iHidroHA

This is a Home Assistant - HA - HACS integration using the [iHidroGo](https://github.com/b247/iHidroGo) — a Go API client for the Hidroelectrica Romania (iHidro) SEW API server.

## License
Copyright (C) 2026 b247_eu, https://b247.eu.org

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://opensource.org/license/gpl-3.0/>.

## What it does
* **Meter Submission Action:** Registers a native Home Assistant action (`ihidro.submit_index`) to transmits an index reading value and can be used in automations or scripts.
* **History Fetching:** Fetch index reading history from the iHidro API (`ihidro.get_index_history`).
---

## Installation
1. Open **HACS** in Home Assistant $\rightarrow$ Click the **3 dots** (top right) $\rightarrow$ **Custom repositories**.
2. Add `https://github.com/b247/iHidroHA` with Type/Category **Integration**.
3. Click **Download**, then restart Home Assistant.
4. Go to **Settings** $\rightarrow$ **Devices & Services** $\rightarrow$ **Add Integration** $\rightarrow$ Search for **iHidro**.
5. Add your iHidro/Hidroelectrica account details and UAN (Contract number).

---

## Usage
Use the registered action in any Home Assistant automation or script:

```yaml
action: ihidro.submit_index
data:
  value: 1050
```

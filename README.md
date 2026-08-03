# iHidroHA

![Home Assistant Integration](https://img.shields.io/badge/Home%20Assistant-Integration-blue.svg)
![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)


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
1. Open **HACS** in Home Assistant &rarr;Click the **3 dots** (top right) &rarr;**Custom repositories**.
2. Add `https://github.com/b247/iHidroHA` with Type/Category **Integration**.
3. Click **Download**, then restart Home Assistant.
4. Go to **Settings** &rarr;**Devices & Services** &rarr;**Add Integration** &rarr;Search for **iHidro**.
5. Add your iHidro/Hidroelectrica account details and UAN (Contract number).



## Usage
Use the registered action in any Home Assistant automation or script:

```yaml
action: ihidro.submit_index
data:
  value: 1050
```
Or manually from **Developer tools** &rarr;**Actions** `ihidro.submit_index`.

A complete HA automation example
---
Triggered by the change (state update) of `input_number.shellypluspmminitgbt_em_offset`— a **Input number helper** created in **Devices & Services** &rarr;**Helpers** 
```yaml
alias: Submit iHidro index and Reset Shelly Monthly Meter
description: ""
triggers:
  - entity_id: input_number.shellypluspmminitgbt_em_offset
    trigger: state
conditions:
  - condition: template
    value_template: "{{ trigger.from_state.state not in ['unavailable', 'unknown'] }}"
  - condition: template
    value_template: "{{ trigger.to_state.state not in ['unavailable', 'unknown'] }}"
actions:
  - action: ihidro.submit_index
    data:
      value: "{{ trigger.to_state.state | int }}"
    response_variable: api_result

  - if:
      - condition: template
        value_template: "{{ api_result.success }}"
    then:
      - action: utility_meter.reset
        target:
          entity_id: sensor.hallway_shellypluspmminitgbt_meter
      - action: persistent_notification.create
        data:
          title: "iHidro Submission Success"
          message: "{{ api_result.output }}"
    else:
      - action: persistent_notification.create
        data:
          title: "iHidro Submission Failed"
          message: "{{ api_result.output }}"
mode: single
```

And a nice dashboard card that hooks the "sendIndex" (actually just open the numeric helper to be updated)
```yaml
type: custom:stack-in-card
title: ""
mode: horizontal
cards:
  - type: gauge
    entity: sensor.hallway_shellypluspmminitgbt_power
    name: ""
    min: 0
    max: 4500
    needle: true
    severity:
      green: 0
      yellow: 900
      red: 2300
    card_mod:
      style: |
        ha-card {
          border-top: 0;
          border-bottom: 0;
        }
  - type: vertical-stack
    cards:
      - type: button
        entity: sensor.hallway_shellypluspmminitgbt_index
        show_name: false
        show_state: true
        show_icon: false
        icon: mdi:transmission-tower
        tap_action:
          action: more-info
        name: ShellyPlusPMMiniTGBT EM Index
        color: var(--secondary-text-color)
        card_mod:
          style: |
            ha-card {
              border:0;
              padding-block-end:unset!important
            }
            ha-card span[class='state'] {
                color: #ffffff;
              }
      - type: button
        entity: input_number.shellypluspmminitgbt_em_offset
        show_name: false
        show_state: false
        show_icon: true
        icon: mdi:transmission-tower-export
        tap_action:
          action: more-info
        name: ShellyPlusPMMiniTGBT EM sync iHidro Oltenitei77 and send Index
        color: var(--secondary-text-color)
        card_mod:
          style: |
            ha-card {
              border: 0;
              padding-block:unset!important
            }
             ha-state-icon {
              color: var(--disabled-text-color) !important;
            }
      - type: button
        entity: sensor.hallway_shellypluspmminitgbt_meter
        show_name: false
        show_state: true
        show_icon: false
        tap_action:
          action: more-info
        name: ShellyPlusPMMiniTGBT Monthly Electricity Consumption Meter
        card_mod:
          style: |
            ha-card {
              border: 0;
              padding-block-start:unset!important
            }
            ha-card span[class='state'] {
              {% set m_kWh = states('sensor.hallway_shellypluspmminitgbt_meter') | float %}
              {% if m_kWh < 90 %}
                color: #4CAF50;  /* Green */
              {% elif m_kWh < 120 %}
                color: #FFB347;  /* Orange: Slightly Cool -> 25 (Ideal) <- Slightly Warm */
              {% else %}
                color: #F98787;  /* Red: Increasing Discomfort / Danger */
              {% endif %}
            }
  - type: gauge
    entity: sensor.hallway_shellypluspmminitgbt_current
    name: ""
    min: 0
    max: 16
    needle: true
    severity:
      green: 0
      yellow: 2
      red: 10
    card_mod:
      style: |
        ha-card {
          border-top: 0;
          border-bottom: 0;
        }

```
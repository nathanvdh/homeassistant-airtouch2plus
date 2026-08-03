# AirTouch 2+ integration

A local Home Assistant integration for Polyaire AirTouch 2+ systems.

This fork is maintained by
[@honeybadger44](https://github.com/honeybadger44) and is based on the original
work by [@nathanvdh](https://github.com/nathanvdh). It uses
[airtouch2-python](https://github.com/nathanvdh/airtouch2-python).

## Entities

| Platform | Description |
|---|---|
| `climate` | AC temperature, mode, setpoint, and fan-speed control |
| `fan` | Zone power and damper-percentage control |

## Installation

1. Select **Download** in HACS.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration**.
4. Search for **AirTouch 2+** and enter the controller's local IP address.

This is an independent community integration and is not an official Polyaire
product.

# AirTouch 2+ integration for Home Assistant

A local Home Assistant integration for the Polyaire AirTouch 2+ controller.
It currently provides climate and zone-fan entities through
[airtouch2-python](https://github.com/nathanvdh/airtouch2-python).

This repository is maintained by
[@honeybadger44](https://github.com/honeybadger44) as a focused fork of
[nathanvdh/homeassistant-airtouch2plus](https://github.com/nathanvdh/homeassistant-airtouch2plus).
Nathan van der Heijden created the original integration and Python library; see
[CREDITS.md](CREDITS.md) for project history.

## Fork goals

- Preserve the existing integration and remain easy to update from upstream.
- Improve automatic polling, reconnect behaviour, and protocol robustness.
- Expose additional local AirTouch 2+ capabilities incrementally.
- Add optional external temperature reporting with automatic native failback.

Home Assistant will supply sensor telemetry only. AirTouch remains responsible
for its normal compressor, mode, fan, setpoint, and safety behaviour.

## Entities

| Platform | Description |
|---|---|
| `climate` | AC temperature, mode, setpoint, and fan-speed control |
| `fan` | Zone power and damper-percentage control |

## Installation

This integration is not included with Home Assistant. Install it through HACS:

1. Add `https://github.com/honeybadger44/homeassistant-airtouch2plus` as a
   custom repository of type **Integration**.
2. Download **AirTouch 2+** through HACS.
3. Restart Home Assistant.
4. Add the AirTouch 2+ integration and enter the controller's local IP address.

See the [HACS custom repository documentation](https://www.hacs.xyz/docs/faq/custom_repositories/)
for more detail.

## Development

Current development happens on focused branches and is recorded in
[CHANGELOG.md](CHANGELOG.md). Nathan's repository is retained as the Git
`upstream` remote so later upstream changes can be reviewed and merged.

This fork is independently maintained and is not an official Polyaire product.

"""Constants for the AirTouch 2+ integration."""

from datetime import timedelta

DOMAIN = "airtouch2plus"

# AirTouch sends updates after control commands, but does not reliably broadcast
# changes made elsewhere. Requesting status keeps Home Assistant current.
STATUS_REFRESH_INTERVAL = timedelta(seconds=5)

# AirTouch zone dampers are much easier to control in useful 5% steps.
ZONE_SPEED_COUNT = 20

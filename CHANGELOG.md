# Changelog

Notable changes to this fork will be recorded here.

## Unreleased

### Changed

- Clarified fork ownership, upstream credit, installation, and project goals.
- Added basic repository housekeeping in preparation for focused development.
- Added a read-only status refresh every five seconds so external changes appear
  in Home Assistant without first operating a control.
- Changed zone airflow controls from 1% to 5% steps.
- Report unavailable current and target temperatures as unavailable instead of
  incorrectly displaying 0 degrees.

### Planned

- Improve reconnect behaviour.
- Add read-only touchpad-temperature reporting.
- Add optional native Touchpad 1 temperature override with automatic failback.

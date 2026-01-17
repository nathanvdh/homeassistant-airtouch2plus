# Airtouch 2+ integration

_Component to integrate with Polyaire Airtouch 2+._

Utilizes [airtouch2-python](https://github.com/nathanvdh/airtouch2-python)

**This component will set up the following platforms.**

Platform | Description
-- | --
`climate` | Control temperature, mode, fan speed

## Installation
This is integration is not available in home assistant by default, it must be either manually copied to your home assistant 'integrations' directory, or installed via HACS (recommended).

See the HACS documentation on how to install it: https://www.hacs.xyz/docs/use

You will then need to add this github repo as a custom repository: https://www.hacs.xyz/docs/faq/custom_repositories

Make sure to select the 'Integration' type.

Download the added custom repository.

The airtouch2plus integration should now appear in the list of integrations with all the others.

When you add the integration, you will be prompted for the host address (IP) of your Airtouch 2+ system - enter it and that's it!

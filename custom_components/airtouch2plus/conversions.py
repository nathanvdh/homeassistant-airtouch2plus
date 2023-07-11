from airtouch2.at2plus import AcMode, AcSetMode, AcFanSpeed

from homeassistant.components.climate import (
    FAN_AUTO,
    FAN_DIFFUSE,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_FOCUS,
    FAN_TOP,
    HVACMode
)

AT2PLUS_TO_HA_MODE = {
    AcMode.AUTO: HVACMode.HEAT_COOL,
    AcMode.HEAT: HVACMode.HEAT,
    AcMode.DRY: HVACMode.DRY,
    AcMode.FAN: HVACMode.FAN_ONLY,
    AcMode.COOL: HVACMode.COOL,
    AcMode.AUTO_HEAT: HVACMode.HEAT, # Unsure what this really is
    AcMode.AUTO_COOL: HVACMode.COOL, # Unsure what this really is
}

AT2PLUS_SETMODE_TO_HA_MODE = {
    AcSetMode.AUTO: HVACMode.HEAT_COOL,
    AcSetMode.HEAT: HVACMode.HEAT,
    AcSetMode.DRY: HVACMode.DRY,
    AcSetMode.FAN: HVACMode.FAN_ONLY,
    AcSetMode.COOL: HVACMode.COOL,
}

AT2PLUS_TO_HA_FAN_SPEED = {
    AcFanSpeed.AUTO: FAN_AUTO,
    AcFanSpeed.QUIET: FAN_DIFFUSE,
    AcFanSpeed.LOW: FAN_LOW,
    AcFanSpeed.MEDIUM: FAN_MEDIUM,
    AcFanSpeed.HIGH: FAN_HIGH,
    AcFanSpeed.POWERFUL: FAN_FOCUS,
    AcFanSpeed.TURBO: FAN_TOP
}

# inverse lookups
HA_MODE_TO_AT2PLUS_SETMODE = {value: key for key,value in AT2PLUS_SETMODE_TO_HA_MODE.items()}
HA_FAN_SPEED_TO_AT2PLUS = {value: key for key, value in AT2PLUS_TO_HA_FAN_SPEED.items()}
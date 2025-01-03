"""Constants for APSystems API."""
# Base component constants
NAME = "APSystems API"
DOMAIN = "apsystems_api"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.0.0"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/patsluth/apsystems-api/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_API_APP_ID = "api_app_id"
CONF_API_APP_SECRET = "api_app_secret"
CONF_SID = "sid"
CONF_ECU_ID = "ecu_id"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

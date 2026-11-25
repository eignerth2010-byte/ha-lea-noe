"""Constants for the unofficial LEA read-only integration."""

DOMAIN = "lea_noe"
NAME = "LEA BOS mobil"
VERSION = "0.1.0"
API_HOST = "https://lea.api.notrufnoe.at"
CONF_PHONE = "phone_number"
CONF_TOKEN = "access_token"
CONF_METHOD = "auth_method"
CONF_INTERVAL = "poll_interval"
CONF_DETAILS = "include_details"
DEFAULT_INTERVAL = 30
MIN_INTERVAL = 30
MAX_INTERVAL = 300
INBOX_LIMIT = 100
INCIDENT_LIMIT = 25
EVENT_TYPES = ["alarm", "information", "cancellation", "message", "unknown"]


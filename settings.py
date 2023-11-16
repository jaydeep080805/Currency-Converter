from os import environ

# window size
APP_WIDTH = 600
APP_HEIGHT = 300
MIN_WIDTH = 400
MIN_HEIGHT = 250

# font
HEADING_FONT = "Verdana"
HEADING_FONT_SIZE = 30
HEADING_FONT_WEIGHT = "bold"

CURRENCY_FONT = "Verdana"
CURRENCY_FONT_SIZE = 16

# access keys
URL = f"http://api.exchangeratesapi.io/v1/latest?access_key={environ.get('ACCESS_KEY')}"

# colors
FG_COLOUR = "#3035c2"
BUTTON_COLOR = "#2a2ead"
BUTTON_COLOR_HOVER = "#25299c"
TRANSPARENT = "transparent"

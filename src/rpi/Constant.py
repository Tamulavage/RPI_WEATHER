from typing import Final
from PyQt5.QtGui import  QFont

REQUEST_TIMEOUT_SECONDS: Final[int] = 1

HOURLY: Final[str] = "Hourly"
DAILY: Final[str] = "Daily"

SMALL_FONT = QFont('Arial',12)
NORMAL_FONT= QFont('Arial', 16)
NORMAL_FONT_BOLD= QFont('Arial', 16, QFont.Bold)
LARGE_FONT= QFont('Arial', 20, QFont.Bold)
XL_FONT_BOLD= QFont('Arial', 40, QFont.Bold)

LIGHT_BLUE= "color: #00e5ff;"
VIVID_RED= "color: #ff001a;"
YELLOW= "color: #FFFF00;"

LOCAL_SENSOR_ON = False
from enum import Enum
from constants import *

class TOOL_ID(Enum):
    HOE = 1
    WATERINGCAN = 2
    SICKLE = 3

class Tool():
    def __init__(self, tool_id):
        self.energy = 1
        self.type = CATEGORY.TOOL
        self.tool = tool_id
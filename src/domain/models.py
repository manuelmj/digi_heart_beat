from enum import Enum 
from dataclasses import dataclass

class StatusInterface(Enum):
    UP = "UP"
    DOWN = "DOWN"

@dataclass
class SystemStatus():
    external_server_status: StatusInterface
    

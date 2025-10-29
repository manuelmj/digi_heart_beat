from enum import Enum 
from dataclasses import dataclass

class StatusInterface(Enum):
    UP = "UP"
    DOWN = "DOWN"

@dataclass
class SystemStatus():
    external_server_status: StatusInterface

    def is_system_up(self) -> bool:
        return self.external_server_status == StatusInterface.UP
    

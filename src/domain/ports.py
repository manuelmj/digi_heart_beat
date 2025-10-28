from abc import ABC, abstractmethod
from domain.models import SystemStatus

class ProtocolServerPort(ABC):
    
    @abstractmethod
    def start(self) -> None:
        """Start the Protocol server."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the Protocol server."""
        pass

class ProtocolClientPort(ABC):
    @abstractmethod
    def read_state(self, address: int) -> int:
        """Read a value from a Protocol register."""
        pass

    @abstractmethod
    def write_state(self, address: int, value: int) -> int:
        """Write a value to a Protocol register."""
        pass

class SystemStatusPort(ABC):
    @abstractmethod
    def get_status(self) -> SystemStatus:
        """Retrieve the current system status."""
        pass
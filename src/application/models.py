from enum import Enum 
from dataclasses import dataclass

# -------------------------------------------------
# MENSAJES DE SOLICITUD
# -------------------------------------------------
@dataclass
class ProtocolRequestReadMessages():
    address: int
    def get_address(self) -> int:
        return self.address
    
@dataclass
class ProtocolRequestWriteMessages():
    address: int
    value_to_write: int

    def get_address(self) -> int:
        return self.address
    def get_value_to_write(self) -> int:
        return self.value_to_write

 
# -------------------------------------------------
# MENSAJES DE RESPUESTA
# -------------------------------------------------

@dataclass
class ProtocolReadMessagesResponse():
    status: bool
    
    def get_status(self) -> bool:
        return self.status

@dataclass
class ProtocolWriteMessagesResponse():
    status: bool

    def get_status(self) -> bool:
        return self.status


    def get_status(self) -> bool:
        return self.status


 
# -------------------------------------------------
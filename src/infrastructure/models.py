from dataclasses import dataclass
from enum import Enum
from typing import Optional 

@dataclass
class EthernetInterface():
    ip: str
    port: int 

@dataclass
class SerialInterface():
    port: str       
    baudrate: int      

@dataclass
class ServerType(Enum):
    TCP = "TCP"
    RTU = "RTU"
    #agregar soporte en siguientes versiones para  udp, rtu, etc. 

@dataclass
class Server():
    type: ServerType 
    ip: str = "127.0.0.1"
    port: int = 502
    timeout: float = 5.0

    def get_host(self) -> str:
        return self.ip
    def get_port(self) -> int:
        return self.port
    def get_timeout(self) -> float:
        return self.timeout
    def get_type(self) -> ServerType:
        return self.type

@dataclass
class ServerInterface():
    servers: list[Server]

    def get_servers(self) -> list[Server]:
        return self.servers


@dataclass
class ICMPIp():
    ip: str
    timeout: float = 2.0

    def get_ip(self) -> str:
        return self.ip
    def get_timeout(self) -> float:
        return self.timeout

@dataclass
class ICMPInterface():
    icmp : list[ICMPIp]

    def get_icmp_ips(self) -> list[ICMPIp]:
        return self.icmp    

class DeviceInterfaces:
    def __init__(self, name: str):
        self.name = name
        self.ethernet: Optional[EthernetInterface] = None
        self.serial: Optional[SerialInterface] = None
        self.server: Optional[ServerInterface] = None
        self.icmp: Optional[ICMPInterface] = None

    def get_ethernet_interface(self) -> Optional[EthernetInterface]:
        return self.ethernet

    def get_serial_interface(self) -> Optional[SerialInterface]:
        return self.serial

    def get_server_interface(self) -> Optional[ServerInterface]:
        return self.server

    def get_icmp_interface(self) -> Optional[ICMPInterface]:
        return self.icmp

    def __repr__(self):
        return (
            f"<DeviceInterfaces name={self.name}, "
            f"ethernet={self.ethernet}, "
            f"serial={self.serial}, "
            f"server={self.server}, "
            f"icmp={self.icmp}>"
        )



class DeviceInterfacesBuilder:
    def __init__(self, name: str):
        self.device = DeviceInterfaces(name)

    def with_ethernet(self, ip: str, port: int):
        self.device.ethernet = EthernetInterface(ip, port)
        return self  

    def with_serial(self, port: str, baudrate: int):
        self.device.serial = SerialInterface(port, baudrate)
        return self


    def with_server(self, servers: list[Server]):
        self.device.server = ServerInterface(servers=servers)
        return self

    def with_icmp(self, icmp_ips: list[ICMPIp]):
        self.device.icmp = ICMPInterface(icmp=icmp_ips)
        return self
 
    def build(self) -> DeviceInterfaces:
        if not any([self.device.ethernet, self.device.serial, self.device.server, self.device.icmp]):
            raise ValueError("Debe configurarse al menos una interfaz de comunicación")
                
        return self.device
 
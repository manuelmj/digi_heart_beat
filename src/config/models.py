from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class ServerConfig():
    """Configuración de un servidor individual"""
    name: str
    host: str
    port: int
    timeout: int
    protocol: str
    enabled: bool
    description: Optional[str]

    def is_enabled(self) -> bool:
        return self.enabled
    def get_host(self) -> str:
        return self.host
    def get_port(self) -> int:
        return self.port
    def get_timeout(self) -> int:
        return self.timeout
    def get_protocol(self) -> str:
        return self.protocol


@dataclass
class ICMPConfig():
    """Configuración de una IP ICMP individual"""
    ip: str
    timeout: int
    enabled: bool
    description: Optional[str]

    def is_enabled(self) -> bool:
        return self.enabled
    def get_ip(self) -> str:
        return self.ip
    def get_timeout(self) -> int:
        return self.timeout
    def get_description(self) -> Optional[str]:
        return self.description


@dataclass
class Config():
    """Configuración completa de la aplicación"""
    servers: List[ServerConfig]
    icmp: List[ICMPConfig]
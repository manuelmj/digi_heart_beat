from infrastructure.modbus_server import ModbusServerAdapter
from infrastructure.modbus_client import ModbusClientAdapter
from infrastructure.system_status import SystemStatusAdapter
from infrastructure.models import DeviceInterfaces,Server, ServerType, DeviceInterfacesBuilder
from application.system_status_actor import SystemStatusActor

from pykka import ActorRef


from application.protocol_actor import ProtocolActor
from pykka import ActorRegistry
import asyncio



class ProtocolComposer:
    @staticmethod
    def compose_modbus_actor(ip: str, port: int, name: str) -> ProtocolActor:
        modbus_server = ModbusServerAdapter(ip=ip, port=port)
        modbus_client = ModbusClientAdapter(ip=ip, port=port)
        protocol_actor = ProtocolActor.start(protocol_server=modbus_server,
                                        protocol_client=modbus_client,
                                        name=name)
        return protocol_actor
    
    @staticmethod
    def compose_system_actor(protocol_actor_ref: ActorRef, system_interval: int) -> SystemStatusActor:
        interfaces = ProtocolComposer._get_interfaces()
        system_status_service = SystemStatusAdapter(interfaces)
        system_status_actor = SystemStatusActor.start(
            system_status_service=system_status_service,
            protocol_actor_ref=protocol_actor_ref,
            system_interval=system_interval,
            name="SystemStatusActor"
        )
        return system_status_actor


    @staticmethod
    def _get_interfaces()-> DeviceInterfaces:
        #construir las interfaces segun sea las configuraciones del proyecto
        
        server1 = Server(type=ServerType.TCP, ip="127.0.0.1", port=5020)
        interfaces = DeviceInterfacesBuilder(name="ModbusDevice")\
                    .with_server(servers=[server1])\
                    .build()
        return interfaces
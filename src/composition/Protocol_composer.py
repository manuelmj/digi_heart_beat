from infrastructure.modbus_server import ModbusServerAdapter
from infrastructure.modbus_client import ModbusClientAdapter
from infrastructure.system_status import SystemStatusAdapter
from infrastructure.models import DeviceInterfaces,Server, ServerType, DeviceInterfacesBuilder
from application.system_status_actor import SystemStatusActor

from pykka import ActorRef
from config.config_loader import ConfigLoader

from application.protocol_actor import ProtocolActor
from pykka import ActorRegistry
 
config = ConfigLoader.load_config()

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
        server_list: list = list()
        
        config_servers = ConfigLoader.get_enabled_servers(config)
        for server in config_servers:
            srv = Server(
                type=ServerType.TCP if server.get_protocol() == "TCP" else ServerType.RTU,
                ip=server.get_host(),
                port=server.get_port(),
                timeout=server.get_timeout()
            )
            server_list.append(srv)

        interfaces = DeviceInterfacesBuilder(name="ModbusDevice")\
                    .with_server(servers=server_list)\
                    .build()
        return interfaces
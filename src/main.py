
from composition.Protocol_composer import ProtocolComposer
from logger import Logger

logger = Logger().get_logger()

def main():  
    """Punto de entrada principal."""
    protocol_actor = ProtocolComposer.compose_modbus_actor(ip="0.0.0.0", port=5020, name ="ModbusProtocolActor")

    ProtocolComposer.compose_system_actor(
        protocol_actor_ref=protocol_actor,
        system_interval=1,
    )



if __name__ == "__main__":
    main()

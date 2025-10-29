from domain.models import SystemStatus, StatusInterface

from domain.ports import SystemStatusPort
import socket

from logger import Logger
_logger = Logger().get_logger()


from infrastructure.models import DeviceInterfaces

class SystemStatusAdapter(SystemStatusPort):

    def __init__(self, interfaces_to_check: DeviceInterfaces):

        if not isinstance(interfaces_to_check, DeviceInterfaces):
            raise TypeError("interfaces_to_check must be an instance of DeviceInterfaces")

        self.interfaces_to_check = interfaces_to_check

    def get_status(self) -> SystemStatus:
        checks = {
        "ethernet": (self.interfaces_to_check.get_ethernet_interface, self._check_ethernet_status),
        "serial": (self.interfaces_to_check.get_serial_interface, self._check_serial_status),
        "server": (self.interfaces_to_check.get_server_interface, self._check_server_status),
        }

        results = {
            name: check_fn()
            for name, (getter, check_fn) in checks.items()
            if getter() is not None
        }
        _logger.debug(f"Resultados de chequear interfaces: {results}")
        if all(results.values()):
            return SystemStatus(StatusInterface.UP)
        else:
            _logger.warning(f"Interfaces con fallo: {[k for k, v in results.items() if not v]}")
            return SystemStatus(StatusInterface.DOWN)


    def _check_ethernet_status(self) -> bool :
        return True


    def _check_serial_status(self) -> bool :
        return True
    #por implementar la logica real para chequear el estado
    
    def _check_server_status(self) -> bool :
        try:

            servers = self.interfaces_to_check.get_server_interface()
            if not servers:
                _logger.warning("No hay interfaces de servidor definidas para chequear el estado Ethernet.")
                return False
            
            result = True
            
            for server in servers.get_servers():
                host = server.get_host()
                port = server.get_port()
                timeout = server.get_timeout()

                try: 
                    with socket.create_connection((host, port), timeout=timeout):
                        _logger.info(f"✅ El servidor Modbus {host}:{port} acepta conexiones.")
                        
                except (socket.timeout, ConnectionRefusedError, OSError) as e:
                    _logger.error(f"❌ No se pudo conectar al servidor {host}:{port}: {e}")
                    result = False
            
            return result  
        except Exception as e:
            _logger.error(f"Error checando estado Ethernet: {str(e)}")
            return False
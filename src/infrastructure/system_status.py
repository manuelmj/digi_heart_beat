from domain.models import SystemStatus, StatusInterface

from domain.ports import SystemStatusPort
import socket
import os 

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
        "icmp": (self.interfaces_to_check.get_icmp_interface, self._check_icmp_status),
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
        
    def _check_icmp_status(self) -> bool :
        try:

            icmp_interface = self.interfaces_to_check.get_icmp_interface()
            if not icmp_interface:
                _logger.warning("No hay interfaces ICMP definidas para chequear el estado.")
                return False
            for icmp_ip in icmp_interface.get_icmp_ips():
                ip = icmp_ip.get_ip()
                timeout = icmp_ip.get_timeout()

                if self.ping(ip, timeout):
                    _logger.info(f"✅ La IP {ip} responde al ping.")
                else:
                    _logger.error(f"❌ La IP {ip} no responde al ping.")
                    return False
            
               
            return True
        except Exception as e:
            _logger.error(f"Error checando estado ICMP: {str(e)}")
            return False
        

    def ping(self,host, timeout):
        """Ping más simple - 1 línea de código"""
        cmd = f"ping -c 1 -W {timeout} {host} > /dev/null 2>&1"
        return os.system(cmd) == 0
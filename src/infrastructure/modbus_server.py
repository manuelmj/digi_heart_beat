# import threading
import time 
from pymodbus.datastore import ModbusServerContext, ModbusSequentialDataBlock, ModbusSimulatorContext
from pymodbus import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer,ServerStop
from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusServerContext,
    ModbusDeviceContext,
    ModbusSequentialDataBlock,
)
from domain.ports import ProtocolServerPort
from logger import Logger

_logger = Logger().get_logger()


class ModbusServerAdapter(ProtocolServerPort):
    """Adaptador para el run_sync_server Modbus"""
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.context = self.setup_server()
        self.server = None

        self.identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
            "ProductName": "Pymodbus Server",
            "ModelName": "Pymodbus Server",
            "MajorMinorRevision": pymodbus_version,
        }
    )




    def start(self):
        """Iniciar el run_sync_server Modbus"""
        self.running = True
        while self.running:  # Cambiado a self.running
            try:
                self.run_sync_server(self.context, self.ip, self.port)
            except Exception as e:
                _logger.error(f"Error en el run_sync_server Modbus: {e}")
            finally:
                time.sleep(5)  # Evitar bucle rápido en caso de error

    def stop(self):
        """Detener el run_sync_server Modbus"""
        if self.running:
            ServerStop()
        self.running = False


    def setup_server(self):
        """Run server setup."""
        context = ModbusDeviceContext(
            hr= ModbusSequentialDataBlock(40001, [0] * 10),
            # co= ModbusSequentialDataBlock(1, [0] * 10),
            # di= ModbusSequentialDataBlock(1, [0] * 10),
            )
        single = True
            # Build data storage
        context = ModbusServerContext(devices=context, single=single)
        _logger.info("Server context ready")
        return context
    
    def run_sync_server(self, context, ip, port) -> None:
        """Run server."""

        txt = f"### start ASYNC server, listening on {port} - {ip}"
        _logger.info(txt)
        _logger.info(f"### start SYNC server, listening on {port} - {ip}")
        
        
        StartTcpServer(
            context= context,  # Data storage
            identity=self.identity,  # server identity
            address=(ip,port),  # listen address
            # custom_functions=[],  # allow custom handling
            # framer=args.framer,  # The framer strategy to use
            # ignore_missing_devices=True,  # ignore request to a missing device
            # broadcast_enable=False,  # treat device_id 0 as broadcast address,
            # timeout=30,  # waiting time for request to complete
        )
        _logger.info("Server shutdown")

from domain.ports import ProtocolClientPort
from typing import Optional
from pymodbus.client import ModbusTcpClient
from typing import List

from logger import Logger
_logger = Logger().get_logger()




class ModbusClientError(Exception):
    """Excepción específica para errores del cliente Modbus"""
    pass



class ModbusClientAdapter(ProtocolClientPort):
    """
   
    """


    def __init__(self, ip: str, port: int = 502):
        """
        Inicializar el adaptador con parámetros de conexión.
        Args:
            ip (str): Dirección IP del servidor Modbus
            port (int): Puerto del servidor Modbus (por defecto 502)
        Raises:
            ValueError: Si los parámetros no son válidos
        """
        if not isinstance(ip, str) or not ip.strip():
            raise ValueError("La IP debe ser una cadena no vacía")
        if not isinstance(port, int) or not (1 <= port <= 65535):
            raise ValueError("El puerto debe ser un entero entre 1 y 65535")
        
        self.ip = ip.strip()
        self.port = port
        self.client: ModbusTcpClient = None
        self._connected = False
        _logger.info(f"Adaptador Holding Register Modbus inicializado para {self.ip}:{self.port}")


    def read_state(self, address: int) -> int:
        """
        Leer un valor de holding register Modbus.
        Args:
            address (int): Dirección del holding register a leer
        Returns:
            int: Valor leído
        """
        if not self._connected:
            self.connect()
          
        try:
            result = self.client.read_holding_registers(address, count=1)
            if result.isError():
                raise ModbusClientError(f"Error leyendo holding register en dirección {address}")
            _logger.info(f"Leído holding register en {address}: {result}")
            result = self.convert_registers_to_int(result.registers)
            return result
        
        except Exception as e:
            error_msg = f"Error leyendo holding register en {address}: {str(e)}"
            _logger.error(error_msg)
            raise ModbusClientError(error_msg) from e

    def write_state(self, address: int, value: int) -> int:
        """
        Escribir un valor en un holding register Modbus.
        Args:
            address (int): Dirección del holding register a escribir
            value (int): Valor a escribir
        Returns:
            int: Resultado de la operación de escritura
        """
        if not self._connected:
            self.connect()
        
        try:
            value = self.convert_int_to_registers(value)
            result = self.client.write_registers(address, value)
            if result.isError():
                raise ModbusClientError(f"Error escribiendo holding register en dirección {address}")
            _logger.info(f"Escrito holding register en {address}: {value}")
            return result
            
        except Exception as e:
            error_msg = f"Error escribiendo holding register en {address}: {str(e)}"
            _logger.error(error_msg)
            raise ModbusClientError(error_msg) from e

      

    def connect(self) -> None:
        """
        Iniciar el cliente Modbus y establecer conexión.
        Crea internamente un ModbusTcpClient con la IP y puerto especificados
        en el constructor y establece la conexión.
        Raises:
            ModbusClientError: Si no se puede establecer la conexión
            ImportError: Si pymodbus no está instalado
        """
        if self._connected:
            return
        
        _logger.info(f"Iniciando cliente Modbus TCP para {self.ip}:{self.port}...")
        
        try:
            # Crear cliente Modbus TCP
            self.client = ModbusTcpClient(
                host=self.ip,
                port=self.port,
                timeout=5,  # Timeout de 5 segundos
                retries=3   # Reintentos automáticos
            )
            # Establecer conexión
            connection_result = self.client.connect()
            if not connection_result:
                raise ModbusClientError(
                    f"No se pudo conectar al servidor Modbus en {self.ip}:{self.port}"
                )
            self._connected = True
            _logger.info(f"Cliente Modbus conectado exitosamente a {self.ip}:{self.port}")
        except ImportError as e:
            error_msg = "pymodbus no está instalado. Instalar con: pip install pymodbus"
            _logger.error(error_msg)
            raise ModbusClientError(error_msg) from e
        except Exception as e:
            error_msg = f"Error iniciando cliente Modbus para {self.ip}:{self.port}: {str(e)}"
            _logger.error(error_msg)
            raise ModbusClientError(error_msg) from e
    
    
    def disconnect(self) -> None:
        """Cerrar la conexión Modbus"""
        if self.client and self._connected:
            self.client.close()
            self._connected = False
            _logger.info("Conexión Modbus cerrada")

    def __del__(self):
        """Destructor para asegurar que se cierra la conexión"""
        
        self.disconnect()



    def convert_registers_to_int(self, registers: list[int]) -> int:
         decoder = ModbusTcpClient.convert_from_registers(
             registers,
             data_type= ModbusTcpClient.DATATYPE.INT16,
             word_order='big'
         )
         return decoder


    def convert_int_to_registers(self, value: int) -> list[int]:
        builder = ModbusTcpClient.convert_to_registers(
            value, data_type=ModbusTcpClient.DATATYPE.INT16, word_order='big'
        )

        return builder

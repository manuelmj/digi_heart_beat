from pykka import ThreadingActor
 
from typing import Union

from application.models import (
    ProtocolReadMessagesResponse,
    ProtocolWriteMessagesResponse,
    ProtocolRequestReadMessages,
    ProtocolRequestWriteMessages,
)

import threading
from domain.ports import (ProtocolServerPort,ProtocolClientPort)

from logger import Logger
logger = Logger().get_logger()


class ProtocolActor(ThreadingActor):
      
    def __init__(self, protocol_server: ProtocolServerPort, protocol_client: ProtocolClientPort, name: str = "ProtocolActor"):
        super().__init__()

        if not isinstance(protocol_server, ProtocolServerPort):
            raise TypeError("protocol_server must implement ProtocolServerPort interface")
    
        if not isinstance(protocol_client, ProtocolClientPort):
            raise TypeError("protocol_client must implement ProtocolClientPort interface")

        self.protocol_server = protocol_server
        self.protocol_client = protocol_client
        self.name = name
        logger.info(f"[{self.name}] initialized.")

    def on_start(self):
        logger.info(f"[{self.name}] Actor started.")
        try: 
            #lanzamos el servidor sincrono en un hilo aparte
            # (para evitar bloquear el hilo del actor)
            self._server_thread = threading.Thread(
                target=self.protocol_server.start,
                name=f"{self.name}-ServerThread",
                daemon=True,
            )
            self._server_thread.start()
            logger.info(f"[{self.name}] Protocol server started in background thread.")
        except Exception as e:
            logger.error(f"[{self.name}] Failed to start protocol server: {e}")

    def on_stop(self):
        logger.info(f"[{self.name}] Actor stopped.")
        try: 
            self.protocol_server.stop()
            logger.info(f"[{self.name}] Protocol server stopped.")
        except Exception as e:
            logger.error(f"[{self.name}] Failed to stop protocol server: {e}")
        #aqui se debe detener el servidor modbus

    def on_failure(self, exception_type, exception_value, traceback):
        logger.error(f"[{self.name}] Actor failed: {exception_value}")

    # -------------------------------------------------
    # RECEPCIÓN DE MENSAJES
    # -------------------------------------------------
    def on_receive(self, message: Union[ProtocolRequestReadMessages, ProtocolRequestWriteMessages]) -> Union[ProtocolReadMessagesResponse, ProtocolWriteMessagesResponse]:
        """
        Método central que maneja todos los mensajes enviados al actor.
        """  
        logger.debug(f"[{self.name}] Received: {message}")

        if isinstance(message, ProtocolRequestReadMessages):
            address = message.get_address()
            result = self.protocol_client.read_state(address=address)
            logger.info(f"[{self.name}] ReadRequest result: {result}")
            return ProtocolReadMessagesResponse(status=bool(result))
        
        elif isinstance(message, ProtocolRequestWriteMessages):
            address = message.get_address()
            value = message.get_value_to_write()
            result = self.protocol_client.write_state(address=address, value=value)
            logger.info(f"[{self.name}] WriteRequest result: {result}")
            return ProtocolWriteMessagesResponse(status=bool(result))
        
        else:
            logger.warning(f"[{self.name}] Unknown command: {cmd}")

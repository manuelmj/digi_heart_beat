

from domain.ports import SystemStatusPort
from application.models import (
    ProtocolRequestReadMessages,
    ProtocolReadMessagesResponse,
    ProtocolRequestWriteMessages,
    ProtocolWriteMessagesResponse,
)

from pykka import ThreadingActor, ActorRef
from logger import Logger
import threading
import time 

_logger = Logger().get_logger()


class SystemStatusActor(ThreadingActor):
      
    def __init__(self, system_status_service: SystemStatusPort,
                protocol_actor_ref: ActorRef,
                system_interval: int,name: str = "SystemStatusActor"):
        super().__init__()

        if not isinstance(system_status_service, SystemStatusPort):
            raise TypeError("system_status_service must implement SystemStatusPort interface")

        if not isinstance(protocol_actor_ref, ActorRef):
            raise TypeError("protocol_actor_ref must be an ActorRef instance")
        
        if system_interval <= 0:
            raise ValueError("system_interval must be a positive integer")

        self.interval = system_interval
        self.target_actor_ref = protocol_actor_ref
        self.system_status_service = system_status_service
        self.name = name
        _logger.info(f"[{self.name}] initialized.")


    def on_start(self):
        _logger.info(f"[{self.name}] Actor started.")

        self._running = True
        self._loop_thread = threading.Thread(
            target=self._loop,
            name=f"{self.name}-LoopThread",
            daemon=True,
        )
        self._loop_thread.start()
        _logger.info(f"[{self.name}] Status loop started in background thread.")

    def on_stop(self):
        self._running = False
        _logger.info(f"[{self.name}] Actor stopped.")


    
    def _loop(self):
        internal_counter = 0
        while self._running:
            try:
                time.sleep(self.interval)
                # Obtener el estado actual
                status = self.system_status_service.get_status()
                _logger.debug(f"[{self.name}] Sending periodic status: {status}")
                
                if status.is_system_up():
                    _logger.info(f"#"*20)
                    _logger.info(f"[{self.name}] System is UP")
                    _logger.info(f"#"*20)
                else:
                    _logger.info(f"#"*20)
                    _logger.warning(f"[{self.name}] System is DOWN")
                    _logger.info(f"#"*20)
                    continue 

                internal_counter += 1

                read_result = self.target_actor_ref.ask(ProtocolRequestReadMessages(address=40001), timeout=10)
                
                if isinstance(read_result, ProtocolReadMessagesResponse):
                    _logger.info(f"Read result: {read_result}")
                else:
                    _logger.error(f"Unexpected result: {read_result}")

                write_result = self.target_actor_ref.ask(ProtocolRequestWriteMessages(address=40001, value_to_write=internal_counter), timeout=10)

                if isinstance(write_result, ProtocolWriteMessagesResponse):
                    _logger.info(f"Write result: {write_result}")
                else:
                    _logger.error(f"Unexpected result: {write_result}")

                if internal_counter == 60:
                    internal_counter = 0

            except Exception as e:
                _logger.error(f"[{self.name}] Error sending status: {e}")
            
            finally:
                time.sleep(self.interval * 2)
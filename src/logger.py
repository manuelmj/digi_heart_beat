import logging
import sys
 
class Logger():
    """Singleton Logger para toda la aplicación."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Configura el logger solo una vez."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        """Devuelve la instancia del logger."""
        return self.logger


import yaml
from typing import List, Dict, Any, Optional
from pathlib import Path
from config.models import Config, ServerConfig

class ConfigLoader:
    """Cargador de configuración desde archivo YAML"""
    
    @staticmethod
    def load_config(config_path: str = "config/config.yml") -> Config:
        """Carga la configuración desde archivo YAML"""
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
            
            with open(config_file, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return Config(**config_data)
            
        except Exception as e:
            raise ValueError(f"Error cargando configuración: {e}")
    
    @staticmethod
    def get_enabled_servers(config: Config) -> List[ServerConfig]:
        """Obtiene solo los servidores habilitados para el ambiente especificado"""   
        
        try: 
            servers = [ServerConfig(**server) for server in config.servers]
            enabled_servers = [server for server in servers if server.is_enabled()]
            return enabled_servers
        except Exception as e:
            raise ValueError(f"Error procesando servidores habilitados: {e}")   

   
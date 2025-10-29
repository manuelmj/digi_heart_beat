from ruamel.yaml import YAML
from typing import List
from pathlib import Path
from config.models import Config, ServerConfig

class ConfigLoader:
    """Cargador de configuración desde archivo YAML (usando ruamel.yaml)"""
    
    @staticmethod
    def load_config(config_path: str = "config.yml") -> Config:
        """Carga la configuración desde archivo YAML"""
        try:
            base_path = Path(__file__).resolve().parent
            absolute_path = (base_path / config_path).resolve()
            if not absolute_path.exists():
                raise FileNotFoundError(f"No se encontró el archivo de configuración: {absolute_path}")

           
            yaml = YAML(typ="safe")
            with open(absolute_path, 'r', encoding='utf-8') as file:
                config_data = yaml.load(file)
            
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

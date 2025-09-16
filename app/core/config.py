"""
Configuration management module for the Weather API application.
Handles loading and validation of configuration from constant.ini file.
"""

import configparser
import os
from pathlib import Path
from typing import Optional


class ConfigurationError(Exception):
    """Raised when there's an error in configuration loading or validation."""
    pass


class Configuration:
    """
    Singleton configuration class that manages application settings.
    Loads configuration from constant.ini file and provides validated access to settings.
    """
    
    _instance: Optional['Configuration'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'Configuration':
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not self._initialized:
            self._config = configparser.ConfigParser()
            self._load_configuration()
            self._validate_configuration()
            Configuration._initialized = True
    
    def _load_configuration(self) -> None:
        """Load configuration from constant.ini file."""
        config_path = Path(__file__).parent.parent.parent / "constant.ini"
        
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found at: {config_path}")
        
        try:
            self._config.read(config_path)
        except configparser.Error as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
    
    def _validate_configuration(self) -> None:
        """Validate that all required configuration values are present."""
        required_sections = ['WEATHER_API', 'LOGGING']
        required_keys = {
            'DEFAULT': ['HOST', 'PORT'],
            'WEATHER_API': ['API_KEY', 'BASE_URL'],
            'LOGGING': ['LOG_LEVEL', 'LOG_FILE']
        }
        
        # Check DEFAULT section keys
        for key in required_keys['DEFAULT']:
            if not self._config.has_option('DEFAULT', key):
                raise ConfigurationError(f"Required key '{key}' not found in DEFAULT section")
        
        # Check other sections
        for section in required_sections:
            if section not in self._config.sections():
                raise ConfigurationError(f"Required section '{section}' not found in configuration")
            
            for key in required_keys[section]:
                if key not in self._config[section]:
                    raise ConfigurationError(f"Required key '{key}' not found in '{section}' section")
        
        # Validate API key is not default
        if self.weather_api_key == "your_weatherapi_key_here":
            raise ConfigurationError("Please set your WeatherAPI key in constant.ini")
    
    @property
    def host(self) -> str:
        """Get the application host."""
        return self._config.get('DEFAULT', 'HOST')
    
    @property
    def port(self) -> int:
        """Get the application port."""
        try:
            return self._config.getint('DEFAULT', 'PORT')
        except ValueError as e:
            raise ConfigurationError(f"Invalid port value: {e}")
    
    @property
    def weather_api_key(self) -> str:
        """Get the WeatherAPI key."""
        return self._config['WEATHER_API']['API_KEY']
    
    @property
    def weather_api_base_url(self) -> str:
        """Get the WeatherAPI base URL."""
        return self._config['WEATHER_API']['BASE_URL']
    
    @property
    def log_level(self) -> str:
        """Get the logging level."""
        return self._config['LOGGING']['LOG_LEVEL']
    
    @property
    def log_file(self) -> str:
        """Get the log file path."""
        return self._config['LOGGING']['LOG_FILE']


# Global configuration instance
config = Configuration()
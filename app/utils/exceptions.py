"""
Custom exceptions for the Weather API application.
Defines specific exception types for different error scenarios.
"""

from typing import Optional, Any, Dict


class WeatherAPIException(Exception):
    """Base exception class for Weather API related errors."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class WeatherAPIConnectionError(WeatherAPIException):
    """Raised when there's a connection error with the WeatherAPI service."""
    
    def __init__(self, message: str = "Failed to connect to WeatherAPI service", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, status_code=503, details=details)


class WeatherAPIAuthenticationError(WeatherAPIException):
    """Raised when there's an authentication error with the WeatherAPI service."""
    
    def __init__(self, message: str = "Invalid API key for WeatherAPI service", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, status_code=401, details=details)


class WeatherAPILocationNotFoundError(WeatherAPIException):
    """Raised when the requested location is not found."""
    
    def __init__(self, location: str, details: Optional[Dict[str, Any]] = None) -> None:
        message = f"Location '{location}' not found"
        super().__init__(message, status_code=404, details=details)


class WeatherAPIRateLimitError(WeatherAPIException):
    """Raised when the API rate limit is exceeded."""
    
    def __init__(self, message: str = "API rate limit exceeded", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, status_code=429, details=details)


class WeatherAPIInvalidParameterError(WeatherAPIException):
    """Raised when invalid parameters are provided to the API."""
    
    def __init__(self, parameter: str, value: Any, details: Optional[Dict[str, Any]] = None) -> None:
        message = f"Invalid parameter '{parameter}' with value '{value}'"
        super().__init__(message, status_code=400, details=details)


class WeatherAPIServiceUnavailableError(WeatherAPIException):
    """Raised when the WeatherAPI service is temporarily unavailable."""
    
    def __init__(self, message: str = "WeatherAPI service is temporarily unavailable", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, status_code=503, details=details)
"""
Weather API endpoints for the FastAPI application.
Defines the REST endpoints for weather data retrieval.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends # type: ignore
from fastapi.responses import JSONResponse # type: ignore

from ..core.logging_config import LoggingConfiguration
from ..services.weather_service import WeatherService
from ..models.response_models import (
    CurrentWeatherResponse,
    HistoryWeatherResponse,
    ForecastWeatherResponse,
    ErrorResponse
)
from ..utils.exceptions import WeatherAPIException


class WeatherAPIRouter:
    """
    Weather API router class that manages all weather-related endpoints.
    Implements dependency injection and proper error handling.
    """
    
    def __init__(self) -> None:
        """Initialize the weather API router."""
        self.router = APIRouter()
        self.logger = LoggingConfiguration.get_logger(__name__)
        self._setup_routes()
    
    def _get_weather_service(self) -> WeatherService:
        """
        Dependency injection for WeatherService.
        Creates a new instance for each request to ensure thread safety.
        
        Returns:
            WeatherService instance
        """
        return WeatherService()
    
    def _handle_weather_api_exception(self, exc: WeatherAPIException) -> JSONResponse:
        """
        Handle WeatherAPI exceptions and return appropriate HTTP responses.
        
        Args:
            exc: WeatherAPI exception
            
        Returns:
            JSONResponse with error details
        """
        self.logger.error(f"WeatherAPI error: {exc.message}")
        
        error_response = ErrorResponse(
            error=exc.__class__.__name__.replace("WeatherAPI", "").replace("Error", ""),
            message=exc.message,
            details=exc.details
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )
    
    def _setup_routes(self) -> None:
        """Set up all weather API routes."""
        
        @self.router.get(
            "/current_weather",
            response_model=CurrentWeatherResponse,
            summary="Get Current Weather",
            description="Fetch current weather details for a given location",
            responses={
                200: {"model": CurrentWeatherResponse},
                400: {"model": ErrorResponse},
                401: {"model": ErrorResponse},
                404: {"model": ErrorResponse},
                429: {"model": ErrorResponse},
                503: {"model": ErrorResponse}
            }
        )
        async def get_current_weather(
            location: str = Query(
                ...,
                description="Name of the city or location (e.g., London, New York, Mumbai)",
                example="London"
            ),
            weather_service: WeatherService = Depends(self._get_weather_service)
        ) -> CurrentWeatherResponse:
            """
            Get current weather for a specific location.
            
            Args:
                location: Location name or coordinates
                weather_service: Injected weather service
                
            Returns:
                Current weather data
            """
            try:
                self.logger.info(f"Current weather request for location: {location}")
                result = await weather_service.get_current_weather(location)
                return result
                
            except WeatherAPIException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Unexpected error in get_current_weather: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        @self.router.get(
            "/history_weather",
            response_model=HistoryWeatherResponse,
            summary="Get Historical Weather",
            description="Fetch past weather data for a given location and number of days",
            responses={
                200: {"model": HistoryWeatherResponse},
                400: {"model": ErrorResponse},
                401: {"model": ErrorResponse},
                404: {"model": ErrorResponse},
                429: {"model": ErrorResponse},
                503: {"model": ErrorResponse}
            }
        )
        async def get_history_weather(
            location: str = Query(
                ...,
                description="Name of the city or location",
                example="Mumbai"
            ),
            days: int = Query(
                ...,
                ge=1,
                le=7,
                description="Number of past days (1-7, as supported by WeatherAPI)",
                example=3
            ),
            weather_service: WeatherService = Depends(self._get_weather_service)
        ) -> HistoryWeatherResponse:
            """
            Get historical weather data for a specific location.
            
            Args:
                location: Location name or coordinates
                days: Number of historical days to retrieve (1-7)
                weather_service: Injected weather service
                
            Returns:
                Historical weather data
            """
            try:
                self.logger.info(f"Historical weather request for location: {location}, days: {days}")
                result = await weather_service.get_history_weather(location, days)
                return result
                
            except WeatherAPIException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Unexpected error in get_history_weather: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        @self.router.get(
            "/forecast",
            response_model=ForecastWeatherResponse,
            summary="Get Weather Forecast",
            description="Fetch weather forecast for a given location with comprehensive data",
            responses={
                200: {"model": ForecastWeatherResponse},
                400: {"model": ErrorResponse},
                401: {"model": ErrorResponse},
                404: {"model": ErrorResponse},
                429: {"model": ErrorResponse},
                503: {"model": ErrorResponse}
            }
        )
        async def get_forecast_weather(
            location: str = Query(
                ...,
                description="Name of the city or location",
                example="New York"
            ),
            days: int = Query(
                3,
                ge=1,
                le=14,
                description="Number of forecast days (1-14, free plan supports up to 3)"
            ),
            hourly: bool = Query(
                False,
                description="Include hourly forecast data"
            ),
            weather_service: WeatherService = Depends(self._get_weather_service)
        ) -> ForecastWeatherResponse:
            """
            Get weather forecast for a specific location.
            
            This endpoint provides comprehensive forecast data including:
            - Daily forecasts with min/max temperatures
            - Weather conditions and precipitation
            - Wind speeds and humidity levels
            - UV index and astronomical data (sunrise/sunset)
            - Optional hourly breakdowns
            
            Args:
                location: Location name or coordinates
                days: Number of forecast days (1-14, free accounts limited to 3)
                hourly: Whether to include hourly forecast data
                weather_service: Injected weather service
                
            Returns:
                Comprehensive forecast weather data
            """
            try:
                self.logger.info(f"Forecast weather request for location: {location}, days: {days}, hourly: {hourly}")
                result = await weather_service.get_forecast_weather(location, days, hourly)
                return result
                
            except WeatherAPIException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Unexpected error in get_forecast_weather: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")
    
    def get_router(self) -> APIRouter:
        """
        Get the configured router instance.
        
        Returns:
            Configured APIRouter instance
        """
        return self.router


# Create router instance
weather_router = WeatherAPIRouter()
router = weather_router.get_router()
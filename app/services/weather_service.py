"""
Weather service module for interacting with WeatherAPI.
Handles all external API communications and data processing.
"""

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, date

from ..core.config import config
from ..core.logging_config import LoggingConfiguration
from ..models.weather_models import (
    WeatherAPICurrentResponse,
    WeatherAPIHistoryResponse,
    WeatherAPIForecastResponse
)
from ..models.response_models import (
    CurrentWeatherResponse,
    HistoryWeatherResponse,
    HistoricalDayData,
    ForecastWeatherResponse,
    ForecastDayData,
    ForecastHourData
)
from ..utils.exceptions import (
    WeatherAPIConnectionError,
    WeatherAPIAuthenticationError,
    WeatherAPILocationNotFoundError,
    WeatherAPIRateLimitError,
    WeatherAPIInvalidParameterError,
    WeatherAPIServiceUnavailableError
)


class WeatherService:
    """
    Service class for interacting with WeatherAPI.
    Handles API requests, response processing, and error handling.
    """
    
    def __init__(self) -> None:
        """Initialize the weather service with configuration and logging."""
        self.logger = LoggingConfiguration.get_logger(__name__)
        self.base_url = config.weather_api_base_url
        self.api_key = config.weather_api_key
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        
        # HTTP client configuration
        self.client_config = {
            "timeout": self.timeout,
            "headers": {
                "User-Agent": "WeatherAPI-FastAPI-Client/1.0"
            }
        }
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an HTTP request to WeatherAPI with proper error handling.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            WeatherAPIException: Various specific exceptions based on error type
        """
        # Add API key to parameters
        params["key"] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        self.logger.info(f"Making request to {endpoint} with params: {params}")
        
        try:
            async with httpx.AsyncClient(**self.client_config) as client:
                response = await client.get(url, params=params)
                
                # Handle different HTTP status codes
                if response.status_code == 200:
                    data = response.json()
                    self.logger.info(f"Successfully received data from {endpoint}")
                    return data
                
                elif response.status_code == 401:
                    self.logger.error("Authentication failed - invalid API key")
                    raise WeatherAPIAuthenticationError()
                
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    error_message = error_data.get("error", {}).get("message", "Invalid request parameters")
                    
                    # Check if it's a location not found error
                    if "No matching location found" in error_message:
                        location = params.get("q", "Unknown")
                        raise WeatherAPILocationNotFoundError(location)
                    else:
                        raise WeatherAPIInvalidParameterError("request", params, {"response": error_data})
                
                elif response.status_code == 429:
                    self.logger.error("API rate limit exceeded")
                    raise WeatherAPIRateLimitError()
                
                elif response.status_code >= 500:
                    self.logger.error(f"WeatherAPI service error: {response.status_code}")
                    raise WeatherAPIServiceUnavailableError()
                
                else:
                    self.logger.error(f"Unexpected response status: {response.status_code}")
                    raise WeatherAPIConnectionError(f"Unexpected response status: {response.status_code}")
        
        except httpx.ConnectError as e:
            self.logger.error(f"Connection error: {e}")
            raise WeatherAPIConnectionError("Failed to connect to WeatherAPI service")
        
        except httpx.TimeoutError as e:
            self.logger.error(f"Request timeout: {e}")
            raise WeatherAPIConnectionError("Request to WeatherAPI service timed out")
        
        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            raise WeatherAPIConnectionError(f"HTTP error occurred: {e}")
    
    async def get_current_weather(self, location: str) -> CurrentWeatherResponse:
        """
        Get current weather for a location.
        
        Args:
            location: Location name (city, coordinates, etc.)
            
        Returns:
            Current weather response
        """
        self.logger.info(f"Getting current weather for location: {location}")
        
        params = {
            "q": location,
            "aqi": "no"  # We don't need air quality data for this endpoint
        }
        
        try:
            data = await self._make_request("current.json", params)
            
            # Parse the response using Pydantic model for validation
            weather_data = WeatherAPICurrentResponse(**data)
            
            # Transform to our response format
            response = CurrentWeatherResponse(
                location_name=weather_data.location.name,
                country=weather_data.location.country,
                local_time=weather_data.location.localtime,
                current_temp_c=weather_data.current.temp_c,
                condition=weather_data.current.condition.text,
                wind_speed_kph=weather_data.current.wind_kph,
                humidity=weather_data.current.humidity
            )
            
            self.logger.info(f"Successfully retrieved current weather for {location}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting current weather for {location}: {e}")
            raise
    
    async def get_history_weather(self, location: str, days: int) -> HistoryWeatherResponse:
        """
        Get historical weather for a location.
        
        Args:
            location: Location name (city, coordinates, etc.)
            days: Number of days to retrieve (1-7)
            
        Returns:
            Historical weather response
        """
        if not 1 <= days <= 7:
            raise WeatherAPIInvalidParameterError("days", days, {"allowed_range": "1-7"})
        
        self.logger.info(f"Getting {days} days of historical weather for location: {location}")
        
        historical_days = []
        
        # Get historical data for each day
        for i in range(1, days + 1):
            target_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            params = {
                "q": location,
                "dt": target_date
            }
            
            try:
                data = await self._make_request("history.json", params)
                
                # Parse the response using Pydantic model for validation
                weather_data = WeatherAPIHistoryResponse(**data)
                
                # Extract the forecast day data
                forecast_day = weather_data.forecast["forecastday"][0]
                
                day_data = HistoricalDayData(
                    date=forecast_day["date"],
                    avg_temp_c=forecast_day["day"]["avgtemp_c"],
                    condition=forecast_day["day"]["condition"]["text"],
                    total_precip_mm=forecast_day["day"]["totalprecip_mm"]
                )
                
                historical_days.append(day_data)
                
            except Exception as e:
                self.logger.error(f"Error getting historical weather for {location} on {target_date}: {e}")
                raise
        
        # Get location info from the last successful request
        response = HistoryWeatherResponse(
            location_name=weather_data.location.name,
            country=weather_data.location.country,
            days=historical_days
        )
        
        self.logger.info(f"Successfully retrieved {days} days of historical weather for {location}")
        return response
    
    async def get_forecast_weather(self, location: str, days: int = 3, include_hourly: bool = False) -> ForecastWeatherResponse:
        """
        Get weather forecast for a location.
        
        Args:
            location: Location name (city, coordinates, etc.)
            days: Number of forecast days (1-14 for paid plans, 1-3 for free)
            include_hourly: Whether to include hourly forecast data
            
        Returns:
            Forecast weather response
        """
        if not 1 <= days <= 14:  # WeatherAPI supports up to 14 days
            raise WeatherAPIInvalidParameterError("days", days, {"allowed_range": "1-14"})
        
        self.logger.info(f"Getting {days} days forecast for location: {location}")
        
        params = {
            "q": location,
            "days": days,
            "aqi": "no",
            "alerts": "no"
        }
        
        try:
            data = await self._make_request("forecast.json", params)
            
            # Parse the response using Pydantic model for validation
            weather_data = WeatherAPIForecastResponse(**data)
            
            # Transform forecast days
            forecast_days = []
            for forecast_day_data in weather_data.forecast["forecastday"]:
                
                # Transform hourly data if requested
                hourly_data = []
                if include_hourly:
                    for hour_data in forecast_day_data["hour"]:
                        hourly_data.append(ForecastHourData(
                            time=hour_data["time"],
                            temp_c=hour_data["temp_c"],
                            condition=hour_data["condition"]["text"],
                            humidity=hour_data["humidity"],
                            wind_kph=hour_data["wind_kph"],
                            precip_mm=hour_data["precip_mm"],
                            chance_of_rain=hour_data["chance_of_rain"]
                        ))
                
                # Extract astronomical data if available
                astro_data = forecast_day_data.get("astro", {})
                sunrise = astro_data.get("sunrise")
                sunset = astro_data.get("sunset")
                
                day_forecast = ForecastDayData(
                    date=forecast_day_data["date"],
                    max_temp_c=forecast_day_data["day"]["maxtemp_c"],
                    min_temp_c=forecast_day_data["day"]["mintemp_c"],
                    avg_temp_c=forecast_day_data["day"]["avgtemp_c"],
                    condition=forecast_day_data["day"]["condition"]["text"],
                    total_precip_mm=forecast_day_data["day"]["totalprecip_mm"],
                    max_wind_kph=forecast_day_data["day"]["maxwind_kph"],
                    avg_humidity=forecast_day_data["day"]["avghumidity"],
                    daily_chance_of_rain=forecast_day_data["day"]["daily_chance_of_rain"],
                    uv_index=forecast_day_data["day"]["uv"],
                    sunrise=sunrise,
                    sunset=sunset,
                    hourly_data=hourly_data
                )
                
                forecast_days.append(day_forecast)
            
            response = ForecastWeatherResponse(
                location_name=weather_data.location.name,
                country=weather_data.location.country,
                current_temp_c=weather_data.current.temp_c,
                current_condition=weather_data.current.condition.text,
                forecast_days=forecast_days
            )
            
            self.logger.info(f"Successfully retrieved {days} days forecast for {location}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting forecast weather for {location}: {e}")
            raise
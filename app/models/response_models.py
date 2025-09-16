"""
Response models for the Weather API endpoints.
Defines the structure of API responses returned to clients.
"""

from datetime import datetime, date
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class CurrentWeatherResponse(BaseModel):
    """Response model for current weather endpoint."""
    location_name: str = Field(..., description="Name of the location")
    country: str = Field(..., description="Country name")
    local_time: str = Field(..., description="Local time at the location")
    current_temp_c: float = Field(..., description="Current temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    wind_speed_kph: float = Field(..., description="Wind speed in kph")
    humidity: int = Field(..., description="Humidity percentage")

    class Config:
        schema_extra = {
            "example": {
                "location_name": "London",
                "country": "United Kingdom",
                "local_time": "2024-01-15 14:30",
                "current_temp_c": 8.5,
                "condition": "Partly cloudy",
                "wind_speed_kph": 15.2,
                "humidity": 72
            }
        }


class HistoricalDayData(BaseModel):
    """Historical weather data for a single day."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    avg_temp_c: float = Field(..., description="Average temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    total_precip_mm: float = Field(..., description="Total precipitation in mm")

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-14",
                "avg_temp_c": 7.2,
                "condition": "Light rain",
                "total_precip_mm": 2.5
            }
        }


class HistoryWeatherResponse(BaseModel):
    """Response model for historical weather endpoint."""
    location_name: str = Field(..., description="Name of the location")
    country: str = Field(..., description="Country name")
    days: List[HistoricalDayData] = Field(..., description="Historical weather data for requested days")

    class Config:
        schema_extra = {
            "example": {
                "location_name": "Mumbai",
                "country": "India",
                "days": [
                    {
                        "date": "2024-01-14",
                        "avg_temp_c": 25.8,
                        "condition": "Sunny",
                        "total_precip_mm": 0.0
                    },
                    {
                        "date": "2024-01-13",
                        "avg_temp_c": 24.2,
                        "condition": "Partly cloudy",
                        "total_precip_mm": 0.5
                    }
                ]
            }
        }


class ForecastHourData(BaseModel):
    """Forecast weather data for a single hour."""
    time: str = Field(..., description="Time in YYYY-MM-DD HH:MM format")
    temp_c: float = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    humidity: int = Field(..., description="Humidity percentage")
    wind_kph: float = Field(..., description="Wind speed in kph")
    precip_mm: float = Field(..., description="Precipitation in mm")
    chance_of_rain: int = Field(..., description="Chance of rain percentage")


class ForecastDayData(BaseModel):
    """Forecast weather data for a single day."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    max_temp_c: float = Field(..., description="Maximum temperature in Celsius")
    min_temp_c: float = Field(..., description="Minimum temperature in Celsius")
    avg_temp_c: float = Field(..., description="Average temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    total_precip_mm: float = Field(..., description="Total precipitation in mm")
    max_wind_kph: float = Field(..., description="Maximum wind speed in kph")
    avg_humidity: float = Field(..., description="Average humidity percentage")
    daily_chance_of_rain: int = Field(..., description="Daily chance of rain percentage")
    uv_index: float = Field(..., description="UV index")
    sunrise: Optional[str] = Field(None, description="Sunrise time")
    sunset: Optional[str] = Field(None, description="Sunset time")
    hourly_data: List[ForecastHourData] = Field([], description="Hourly forecast data")


class ForecastWeatherResponse(BaseModel):
    """Response model for forecast weather endpoint."""
    location_name: str = Field(..., description="Name of the location")
    country: str = Field(..., description="Country name")
    current_temp_c: float = Field(..., description="Current temperature in Celsius")
    current_condition: str = Field(..., description="Current weather condition")
    forecast_days: List[ForecastDayData] = Field(..., description="Forecast data for requested days")

    class Config:
        schema_extra = {
            "example": {
                "location_name": "New York",
                "country": "United States of America",
                "current_temp_c": 5.2,
                "current_condition": "Snow",
                "forecast_days": [
                    {
                        "date": "2024-01-15",
                        "max_temp_c": 6.8,
                        "min_temp_c": -1.2,
                        "avg_temp_c": 2.8,
                        "condition": "Light snow",
                        "total_precip_mm": 15.5,
                        "max_wind_kph": 25.2,
                        "avg_humidity": 85.0,
                        "daily_chance_of_rain": 20,
                        "uv_index": 1.5,
                        "sunrise": "07:15",
                        "sunset": "17:05",
                        "hourly_data": []
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

    class Config:
        schema_extra = {
            "example": {
                "error": "LocationNotFound",
                "message": "Location 'InvalidCity' not found",
                "details": {
                    "requested_location": "InvalidCity",
                    "suggestions": ["Please check the spelling and try again"]
                }
            }
        }
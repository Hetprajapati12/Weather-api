"""
Pydantic models for weather data validation and serialization.
Defines the structure for API requests and responses.
"""

from datetime import datetime, date
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator, root_validator


class WeatherCondition(BaseModel):
    """Weather condition information."""
    text: str = Field(..., description="Weather condition text")
    icon: str = Field(..., description="Weather condition icon URL")
    code: int = Field(..., description="Weather condition code")


class Location(BaseModel):
    """Location information."""
    name: str = Field(..., description="Location name")
    region: str = Field(..., description="Region/state")
    country: str = Field(..., description="Country name")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    tz_id: str = Field(..., description="Timezone identifier")
    localtime_epoch: int = Field(..., description="Local time as epoch")
    localtime: str = Field(..., description="Local time as string")


class CurrentWeather(BaseModel):
    """Current weather data."""
    last_updated_epoch: int = Field(..., description="Last updated time as epoch")
    last_updated: str = Field(..., description="Last updated time as string")
    temp_c: float = Field(..., description="Temperature in Celsius")
    temp_f: float = Field(..., description="Temperature in Fahrenheit")
    is_day: int = Field(..., description="Whether it's day (1) or night (0)")
    condition: WeatherCondition = Field(..., description="Weather condition")
    wind_mph: float = Field(..., description="Wind speed in mph")
    wind_kph: float = Field(..., description="Wind speed in kph")
    wind_degree: int = Field(..., description="Wind direction in degrees")
    wind_dir: str = Field(..., description="Wind direction")
    pressure_mb: float = Field(..., description="Pressure in millibars")
    pressure_in: float = Field(..., description="Pressure in inches")
    precip_mm: float = Field(..., description="Precipitation in mm")
    precip_in: float = Field(..., description="Precipitation in inches")
    humidity: int = Field(..., description="Humidity percentage")
    cloud: int = Field(..., description="Cloud cover percentage")
    feelslike_c: float = Field(..., description="Feels like temperature in Celsius")
    feelslike_f: float = Field(..., description="Feels like temperature in Fahrenheit")
    vis_km: float = Field(..., description="Visibility in km")
    vis_miles: float = Field(..., description="Visibility in miles")
    uv: float = Field(..., description="UV Index")
    gust_mph: float = Field(..., description="Gust speed in mph")
    gust_kph: float = Field(..., description="Gust speed in kph")


class DayWeather(BaseModel):
    """Day weather data for historical/forecast."""
    maxtemp_c: float = Field(..., description="Maximum temperature in Celsius")
    maxtemp_f: float = Field(..., description="Maximum temperature in Fahrenheit")
    mintemp_c: float = Field(..., description="Minimum temperature in Celsius")
    mintemp_f: float = Field(..., description="Minimum temperature in Fahrenheit")
    avgtemp_c: float = Field(..., description="Average temperature in Celsius")
    avgtemp_f: float = Field(..., description="Average temperature in Fahrenheit")
    maxwind_mph: float = Field(..., description="Maximum wind speed in mph")
    maxwind_kph: float = Field(..., description="Maximum wind speed in kph")
    totalprecip_mm: float = Field(..., description="Total precipitation in mm")
    totalprecip_in: float = Field(..., description="Total precipitation in inches")
    totalsnow_cm: float = Field(..., description="Total snow in cm")
    avgvis_km: float = Field(..., description="Average visibility in km")
    avgvis_miles: float = Field(..., description="Average visibility in miles")
    avghumidity: float = Field(..., description="Average humidity percentage")
    daily_will_it_rain: int = Field(..., description="Will it rain (1) or not (0)")
    daily_chance_of_rain: int = Field(..., description="Chance of rain percentage")
    daily_will_it_snow: int = Field(..., description="Will it snow (1) or not (0)")
    daily_chance_of_snow: int = Field(..., description="Chance of snow percentage")
    condition: WeatherCondition = Field(..., description="Weather condition")
    uv: float = Field(..., description="UV Index")


class HourWeather(BaseModel):
    """Hourly weather data."""
    time_epoch: int = Field(..., description="Time as epoch")
    time: str = Field(..., description="Time as string")
    temp_c: float = Field(..., description="Temperature in Celsius")
    temp_f: float = Field(..., description="Temperature in Fahrenheit")
    is_day: int = Field(..., description="Whether it's day (1) or night (0)")
    condition: WeatherCondition = Field(..., description="Weather condition")
    wind_mph: float = Field(..., description="Wind speed in mph")
    wind_kph: float = Field(..., description="Wind speed in kph")
    wind_degree: int = Field(..., description="Wind direction in degrees")
    wind_dir: str = Field(..., description="Wind direction")
    pressure_mb: float = Field(..., description="Pressure in millibars")
    pressure_in: float = Field(..., description="Pressure in inches")
    precip_mm: float = Field(..., description="Precipitation in mm")
    precip_in: float = Field(..., description="Precipitation in inches")
    humidity: int = Field(..., description="Humidity percentage")
    cloud: int = Field(..., description="Cloud cover percentage")
    feelslike_c: float = Field(..., description="Feels like temperature in Celsius")
    feelslike_f: float = Field(..., description="Feels like temperature in Fahrenheit")
    windchill_c: float = Field(..., description="Wind chill in Celsius")
    windchill_f: float = Field(..., description="Wind chill in Fahrenheit")
    heatindex_c: float = Field(..., description="Heat index in Celsius")
    heatindex_f: float = Field(..., description="Heat index in Fahrenheit")
    dewpoint_c: float = Field(..., description="Dew point in Celsius")
    dewpoint_f: float = Field(..., description="Dew point in Fahrenheit")
    vis_km: float = Field(..., description="Visibility in km")
    vis_miles: float = Field(..., description="Visibility in miles")
    uv: float = Field(..., description="UV Index")
    gust_mph: float = Field(..., description="Gust speed in mph")
    gust_kph: float = Field(..., description="Gust speed in kph")
    will_it_rain: int = Field(..., description="Will it rain (1) or not (0)")
    chance_of_rain: int = Field(..., description="Chance of rain percentage")
    will_it_snow: int = Field(..., description="Will it snow (1) or not (0)")
    chance_of_snow: int = Field(..., description="Chance of snow percentage")


class ForecastDay(BaseModel):
    """Forecast day data."""
    date: str = Field(..., description="Date as string (YYYY-MM-DD)")
    date_epoch: int = Field(..., description="Date as epoch")
    day: DayWeather = Field(..., description="Day weather data")
    astro: Optional[dict] = Field(None, description="Astronomical data")
    hour: List[HourWeather] = Field(..., description="Hourly weather data")


class WeatherAPICurrentResponse(BaseModel):
    """Complete current weather API response."""
    location: Location = Field(..., description="Location information")
    current: CurrentWeather = Field(..., description="Current weather data")


class WeatherAPIHistoryResponse(BaseModel):
    """Complete historical weather API response."""
    location: Location = Field(..., description="Location information")
    forecast: dict = Field(..., description="Forecast data containing forecastday list")


class WeatherAPIForecastResponse(BaseModel):
    """Complete forecast weather API response."""
    location: Location = Field(..., description="Location information")
    current: CurrentWeather = Field(..., description="Current weather data")
    forecast: dict = Field(..., description="Forecast data containing forecastday list")
# Weather API - FastAPI Assignment

A professional REST API built with FastAPI that integrates with WeatherAPI.com to provide comprehensive weather information. This application demonstrates enterprise-level best practices including proper OOP design, configuration management, error handling, and logging.

## Features

- **Current Weather**: Get real-time weather data for any location
- **Historical Weather**: Access past weather data (up to 7 days)
- **Weather Forecast**: Comprehensive forecast data with optional hourly breakdowns
- **Professional Architecture**: Clean separation of concerns with services, models, and API layers
- **Robust Error Handling**: Comprehensive exception handling with meaningful error messages
- **Configuration Management**: External configuration via INI file
- **Structured Logging**: File rotation and console output with detailed formatting
- **Input Validation**: Pydantic models for request/response validation
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Project Structure

```
weather_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application and server setup
│   ├── api/
│   │   ├── __init__.py
│   │   └── weather.py          # Weather API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   └── logging_config.py   # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── weather_models.py   # WeatherAPI response models
│   │   └── response_models.py  # API response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather_service.py  # Business logic and API integration
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py       # Custom exceptions
├── constant.ini                # Configuration file
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore rules
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- WeatherAPI.com API key (free account)

### Installation

1. **Clone or create the project structure**
   ```bash
   mkdir weather_api
   cd weather_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get WeatherAPI Key**
   - Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
   - Get your free API key from the dashboard

5. **Configure the application**
   
   Update `constant.ini` with your API key:
   ```ini
   [DEFAULT]
   HOST = 127.0.0.1
   PORT = 8000

   [WEATHER_API]
   API_KEY = your_actual_api_key_here
   BASE_URL = https://api.weatherapi.com/v1

   [LOGGING]
   LOG_LEVEL = INFO
   LOG_FILE = weather_api.log
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

##  API Endpoints

### Base URL
```
http://127.0.0.1:8000
```

### Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Weather API is running",
  "version": "1.0.0"
}
```

### 1. Current Weather
```
GET /current_weather?location={location}
```

**Parameters:**
- `location` (required): City name, coordinates, or location identifier

**Example:**
```bash
curl "http://127.0.0.1:8000/current_weather?location=London"
```

**Response:**
```json
{
  "location_name": "London",
  "country": "United Kingdom",
  "local_time": "2024-01-15 14:30",
  "current_temp_c": 8.5,
  "condition": "Partly cloudy",
  "wind_speed_kph": 15.2,
  "humidity": 72
}
```

### 2. Historical Weather
```
GET /history_weather?location={location}&days={days}
```

**Parameters:**
- `location` (required): City name, coordinates, or location identifier
- `days` (required): Number of past days (1-7)

**Example:**
```bash
curl "http://127.0.0.1:8000/history_weather?location=Mumbai&days=3"
```

**Response:**
```json
{
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
```

### 3. Weather Forecast
```
GET /forecast?location={location}&days={days}&hourly={hourly}
```

**Parameters:**
- `location` (required): City name, coordinates, or location identifier
- `days` (optional): Number of forecast days (default: 3, max: 14 for paid plans)
- `hourly` (optional): Include hourly forecast data (default: false)

**Example:**
```bash
curl "http://127.0.0.1:8000/forecast?location=New York&days=2&hourly=false"
```

**Response:**
```json
{
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
```

## Error Handling

The API provides comprehensive error handling with meaningful messages:

**Error Response Format:**
```json
{
  "error": "LocationNotFound",
  "message": "Location 'InvalidCity' not found",
  "details": {
    "requested_location": "InvalidCity"
  }
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (invalid API key)
- `404`: Not Found (location not found)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error
- `503`: Service Unavailable (WeatherAPI down)

## Configuration

### Configuration File Structure

The `constant.ini` file contains all application settings:

```ini
[DEFAULT]
HOST = 127.0.0.1          # Server host
PORT = 8000               # Server port

[WEATHER_API]
API_KEY = your_key_here   # WeatherAPI.com API key
BASE_URL = https://api.weatherapi.com/v1  # WeatherAPI base URL

[LOGGING]
LOG_LEVEL = INFO          # Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE = weather_api.log # Log file path
```

### WeatherAPI Limits (Free Plan)

- **1 million API calls per month**
- **Current weather data**
- **3-day weather forecast**
- **Historical weather data** (up to 7 days back)
- **Search/Autocomplete**

## Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
httpx==0.25.2
python-multipart==0.0.6
configparser==6.0.0
```

## Architecture

This application follows enterprise-level design patterns:

### Object-Oriented Design
- **Configuration Class**: Singleton pattern for configuration management
- **Service Classes**: Encapsulate business logic and external API communication
- **Router Classes**: Organize API endpoints with dependency injection

### Pydantic Models
- **Input Validation**: Automatic request validation
- **Output Serialization**: Consistent response formatting
- **Type Safety**: Full type hints throughout the application

### Error Handling
- **Custom Exceptions**: Specific exception types for different error scenarios
- **Global Exception Handlers**: Centralized error processing
- **Structured Error Responses**: Consistent error format across all endpoints

### Logging
- **Structured Logging**: Detailed log format with timestamps and context
- **File Rotation**: Automatic log file rotation (10MB max, 5 backups)
- **Multiple Handlers**: Console and file logging
- **Configurable Levels**: Adjustable logging verbosity

##  Testing

### Using Interactive Documentation
1. Start the server
2. Visit http://127.0.0.1:8000/docs
3. Click "Try it out" on any endpoint
4. Enter parameters and click "Execute"

### Using cURL
```bash
# Test health endpoint
curl "http://127.0.0.1:8000/health"

# Test current weather
curl "http://127.0.0.1:8000/current_weather?location=London"

# Test historical weather
curl "http://127.0.0.1:8000/history_weather?location=Mumbai&days=2"

# Test forecast
curl "http://127.0.0.1:8000/forecast?location=Tokyo&days=3&hourly=true"
```

### Using Python Requests
```python
import requests

base_url = "http://127.0.0.1:8000"

# Test current weather
response = requests.get(f"{base_url}/current_weather?location=London")
print(response.json())

# Test forecast
response = requests.get(f"{base_url}/forecast?location=Paris&days=3")
print(response.json())
```

##  Development

### Running in Development Mode
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Logging
- Check `weather_api.log` for detailed application logs
- Set `LOG_LEVEL = DEBUG` in `constant.ini` for verbose logging

### Adding New Features
1. **Models**: Add Pydantic models in `app/models/`
2. **Services**: Implement business logic in `app/services/`
3. **APIs**: Create endpoints in `app/api/`
4. **Exceptions**: Define custom exceptions in `app/utils/exceptions.py`

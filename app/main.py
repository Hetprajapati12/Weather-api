"""
Main FastAPI application module.
Initializes the application, sets up middleware, and configures routes.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse # type: ignore
import uvicorn # type: ignore

from .core.config import config, ConfigurationError
from .core.logging_config import LoggingConfiguration
from .api.weather import router as weather_router
from .utils.exceptions import WeatherAPIException


class WeatherAPIApplication:
    """
    Main application class that configures and initializes the FastAPI app.
    Follows enterprise-level patterns for application lifecycle management.
    """
    
    def __init__(self) -> None:
        """Initialize the weather API application."""
        # Setup logging first
        LoggingConfiguration.setup_logging()
        self.logger = LoggingConfiguration.get_logger(__name__)
        
        # Create FastAPI app with lifespan
        self.app = FastAPI(
            title="Weather API",
            description="A professional REST API for weather data using WeatherAPI.com",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
            lifespan=self._lifespan
        )
        
        self._setup_middleware()
        self._setup_routes()
        self._setup_exception_handlers()
    
    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
        """
        Application lifespan manager.
        Handles startup and shutdown events.
        """
        # Startup
        self.logger.info("Starting Weather API application...")
        try:
            # Validate configuration on startup
            self.logger.info("Configuration validated successfully")
            self.logger.info(f"Weather API configured with base URL: {config.weather_api_base_url}")
            yield
        except ConfigurationError as e:
            self.logger.error(f"Configuration error during startup: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during startup: {e}")
            raise
        finally:
            # Shutdown
            self.logger.info("Shutting down Weather API application...")
    
    def _setup_middleware(self) -> None:
        """Set up application middleware."""
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["GET"],
            allow_headers=["*"],
        )
        
        # Request logging middleware
        @self.app.middleware("http")
        async def log_requests(request: Request, call_next):
            """Log all HTTP requests and responses."""
            self.logger.info(f"Incoming request: {request.method} {request.url}")
            
            try:
                response = await call_next(request)
                self.logger.info(f"Response status: {response.status_code}")
                return response
            except Exception as e:
                self.logger.error(f"Request processing error: {e}")
                raise
    
    def _setup_routes(self) -> None:
        """Set up application routes."""
        # Health check endpoint
        @self.app.get(
            "/health",
            summary="Health Check",
            description="Check if the API is running and healthy",
            tags=["System"]
        )
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "message": "Weather API is running",
                "version": "1.0.0"
            }
        
        # Include weather router
        self.app.include_router(
            weather_router,
            tags=["Weather"],
            responses={
                500: {"description": "Internal Server Error"},
                503: {"description": "Service Unavailable"}
            }
        )
    
    def _setup_exception_handlers(self) -> None:
        """Set up global exception handlers."""
        
        @self.app.exception_handler(WeatherAPIException)
        async def weather_api_exception_handler(request: Request, exc: WeatherAPIException):
            """Handle WeatherAPI specific exceptions."""
            self.logger.error(f"WeatherAPI exception: {exc.message}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": exc.__class__.__name__.replace("WeatherAPI", "").replace("Error", ""),
                    "message": exc.message,
                    "details": exc.details
                }
            )
        
        @self.app.exception_handler(ConfigurationError)
        async def configuration_exception_handler(request: Request, exc: ConfigurationError):
            """Handle configuration errors."""
            self.logger.error(f"Configuration error: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "ConfigurationError",
                    "message": "Application configuration error",
                    "details": {"error": str(exc)}
                }
            )
        
        @self.app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            """Handle all other exceptions."""
            self.logger.error(f"Unhandled exception: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "details": {}
                }
            )
    
    def get_app(self) -> FastAPI:
        """
        Get the configured FastAPI application instance.
        
        Returns:
            Configured FastAPI application
        """
        return self.app


# Create application instance
weather_app = WeatherAPIApplication()
app = weather_app.get_app()


def main() -> None:
    """
    Main entry point for running the application.
    Used when running directly with Python.
    """
    try:
        LoggingConfiguration.setup_logging()
        logger = LoggingConfiguration.get_logger(__name__)
        
        logger.info("Starting Weather API server...")
        logger.info(f"Server will run on {config.host}:{config.port}")
        
        uvicorn.run(
            "app.main:app",
            host=config.host,
            port=config.port,
            reload=False,  # Set to True for development
            log_config=None,  # Use our custom logging
        )
        
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to start server: {e}")
        exit(1)


if __name__ == "__main__":
    main()
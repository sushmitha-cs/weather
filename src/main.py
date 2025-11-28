import sys
import os
import time
import logging

# Add lib to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))

from src.weather_service import WeatherService
from src.display_service import DisplayService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Weather Display...")
    weather_service = WeatherService()
    display_service = DisplayService()

    try:
        while True:
            logger.info("Fetching weather data...")
            weather = weather_service.get_current_weather()
            
            if weather:
                logger.info(f"Weather fetched: {weather}")
                logger.info("Updating display...")
                display_service.update_display(weather)
            else:
                logger.error("Failed to fetch weather data")

            # Sleep for 30 minutes
            logger.info("Sleeping for 30 minutes...")
            time.sleep(1800) 
            
    except KeyboardInterrupt:
        logger.info("Exiting...")
        display_service.clear()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        display_service.clear()

if __name__ == "__main__":
    main()

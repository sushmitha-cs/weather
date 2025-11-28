import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont

# Ensure lib is in path if running directly (for testing)
if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))

try:
    from waveshare_epd import epd2in13_V4
except (ImportError, RuntimeError, Exception) as e:
    # Mock for testing on non-Pi systems or if driver fails to init
    print(f"Warning: waveshare_epd driver could not be loaded ({e}). Using mock.")
    class MockEPD:
        width = 122
        height = 250
        def init(self): pass
        def Clear(self, color): pass
        def display(self, image): pass
        def getbuffer(self, image): return []
        def sleep(self): pass
    
    class MockModule:
        EPD = MockEPD
    
    epd2in13_V4 = MockModule()

class DisplayService:
    def __init__(self):
        self.epd = epd2in13_V4.EPD()
        self.epd.init()
        self.epd.Clear(0xFF)
        # Use default font for simplicity
        self.font = ImageFont.load_default()

    def update_display(self, weather_data):
        if not weather_data:
            return
        
        # Create image with swapped dimensions because we will rotate it or the driver handles it
        # The driver's getbuffer expects image size to match width/height or height/width
        # EPD_WIDTH = 122, EPD_HEIGHT = 250
        # We usually draw in landscape mode (250x122)
        
        image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        temp = weather_data.get('temperature')
        wind = weather_data.get('windspeed')
        code = weather_data.get('weathercode')
        
        draw.text((10, 10), f"Temp: {temp} C", font=self.font, fill=0)
        draw.text((10, 30), f"Wind: {wind} km/h", font=self.font, fill=0)
        draw.text((10, 50), f"Code: {code}", font=self.font, fill=0)
        
        self.epd.display(self.epd.getbuffer(image))

    def clear(self):
        self.epd.Clear(0xFF)
        self.epd.sleep()

if __name__ == "__main__":
    ds = DisplayService()
    # Test data
    ds.update_display({'temperature': 20, 'windspeed': 10, 'weathercode': 1})

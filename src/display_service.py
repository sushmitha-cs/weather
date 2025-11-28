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

try:
    from src.icons import IconDrawer
except ImportError:
    from icons import IconDrawer

class DisplayService:
    def __init__(self):
        self.epd = epd2in13_V4.EPD()
        self.epd.init()
        self.epd.Clear(0xFF)
        # Use default font for simplicity
        self.font = ImageFont.load_default()
        # Try to load fonts (Linux/Pi usually has DejaVuSans, Windows has Arial)
        try:
            # Bold fonts for headers/main info
            self.font_location = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
            self.font_temp = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            self.font_detail = ImageFont.truetype("DejaVuSans.ttf", 18)
        except IOError:
            try:
                # Fallback for Windows
                self.font_location = ImageFont.truetype("arialbd.ttf", 24)
                self.font_temp = ImageFont.truetype("arialbd.ttf", 36)
                self.font_detail = ImageFont.truetype("arial.ttf", 18)
            except IOError:
                # Ultimate fallback
                self.font_location = ImageFont.load_default()
                self.font_temp = ImageFont.load_default()
                self.font_detail = ImageFont.load_default()

    def update_display(self, weather_data, location_name="Weather"):
        if not weather_data:
            return
        
        # EPD_WIDTH = 122, EPD_HEIGHT = 250
        # Landscape mode: 250x122
        width = self.epd.height
        height = self.epd.width
        
        image = Image.new('1', (width, height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        icon_drawer = IconDrawer(draw)

        temp = weather_data.get('temperature')
        wind = weather_data.get('windspeed')
        code = weather_data.get('weathercode')
        
        # --- Layout ---
        
        # 1. Location Name (Centered Top)
        # Calculate text width to center it
        bbox = draw.textbbox((0, 0), location_name, font=self.font_location)
        text_width = bbox[2] - bbox[0]
        x_loc = (width - text_width) // 2
        draw.text((x_loc, 2), location_name, font=self.font_location, fill=0)

        # 2. Icon (Left side, large)
        icon_size = 90
        icon_y = 30
        icon_x = 10
        icon_drawer.draw_icon_for_code(code, icon_x, icon_y, icon_size)
        
        # 3. Temperature (Right side, large)
        temp_c = temp
        temp_f = (temp_c * 9/5) + 32
        temp_str = f"{int(temp_f)}°F" # Emphasize F, or show both compactly
        # Let's show "68°F" large, and "20°C" smaller below or beside?
        # User asked for both previously. Let's try to fit "20°C | 68°F" if it fits, or stack them.
        # Given "make best use of space", large text is better.
        # Let's do:
        # 20°C
        # 68°F
        
        text_x = 110
        draw.text((text_x, 35), f"{temp_c}°C", font=self.font_temp, fill=0)
        draw.text((text_x, 70), f"{int(temp_f)}°F", font=self.font_temp, fill=0)
        
        # 4. Details (Wind) - Bottom Right or below location?
        # Let's put wind below location or in the corner.
        # Space is tight with two large temps.
        # Alternative: "20°C / 68°F" as one line might be too wide for 36pt.
        # Let's try a slightly smaller font for temp if we want both on one line, OR stack them.
        # Stacking seems good.
        
        # Wind
        draw.text((text_x + 80, 55), f"Wind\n{wind}\nkm/h", font=self.font_detail, fill=0)
        
        # Actually, let's refine:
        # Icon | Temp C / Temp F
        #      | Wind
        
        # Redoing layout for cleaner look:
        image = Image.new('1', (width, height), 255)
        draw = ImageDraw.Draw(image)
        icon_drawer = IconDrawer(draw)
        
        # Header
        bbox = draw.textbbox((0, 0), location_name, font=self.font_location)
        text_width = bbox[2] - bbox[0]
        x_loc = (width - text_width) // 2
        draw.text((x_loc, 0), location_name, font=self.font_location, fill=0)
        
        # Divider line
        draw.line((0, 28, width, 28), fill=0, width=2)
        
        # Icon
        icon_size = 80
        icon_drawer.draw_icon_for_code(code, 5, 35, icon_size)
        
        # Info Area starts at x=90
        info_x = 95
        
        # Temp
        temp_text = f"{temp_c}°C  {int(temp_f)}°F"
        draw.text((info_x, 35), temp_text, font=self.font_location, fill=0) # Use 24pt bold for temp line
        
        # 4. Details
        # Wind
        wind_dir = weather_data.get('winddirection', 0)
        def get_cardinal(d):
            dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            ix = round(d / (360. / len(dirs)))
            return dirs[ix % len(dirs)]
        
        wind_cardinal = get_cardinal(wind_dir)
        
        draw.text((info_x, 65), f"Wind: {wind} km/h {wind_cardinal}", font=self.font_detail, fill=0)
        
        # Time / Update status
        time_str = weather_data.get('time', '').split('T')[-1] # Extract HH:MM
        draw.text((info_x, 85), f"Updated: {time_str}", font=self.font_detail, fill=0)
        
        self.epd.display(self.epd.getbuffer(image))

    def clear(self):
        self.epd.Clear(0xFF)
        self.epd.sleep()

if __name__ == "__main__":
    ds = DisplayService()
    # Test data
    ds.update_display({'temperature': 20, 'windspeed': 10, 'weathercode': 1})

from PIL import ImageDraw

class IconDrawer:
    def __init__(self, draw: ImageDraw.ImageDraw):
        self.draw = draw

    def draw_sun(self, x, y, size):
        """Draws a sun icon."""
        r = size // 2
        cx, cy = x + r, y + r
        # Core
        self.draw.ellipse((cx - r//2, cy - r//2, cx + r//2, cy + r//2), fill=0)
        # Rays
        ray_len = r // 3
        for i in range(0, 360, 45):
            import math
            rad = math.radians(i)
            x1 = cx + (r//2 + 2) * math.cos(rad)
            y1 = cy + (r//2 + 2) * math.sin(rad)
            x2 = cx + (r//2 + 2 + ray_len) * math.cos(rad)
            y2 = cy + (r//2 + 2 + ray_len) * math.sin(rad)
            self.draw.line((x1, y1, x2, y2), fill=0, width=2)

    def draw_cloud(self, x, y, size):
        """Draws a cloud icon."""
        # Simple cloud made of circles
        r = size // 3
        self.draw.ellipse((x, y + r, x + 2*r, y + 3*r), fill=0)
        self.draw.ellipse((x + r, y, x + 3*r, y + 2*r), fill=0)
        self.draw.ellipse((x + 2*r, y + r, x + 4*r, y + 3*r), fill=0)
        # Fill gaps
        self.draw.rectangle((x + r, y + r, x + 3*r, y + 2.5*r), fill=0)

    def draw_rain(self, x, y, size):
        """Draws a rain cloud."""
        self.draw_cloud(x, y, size)
        # Rain drops
        drop_len = size // 4
        start_y = y + size
        for i in range(3):
            dx = x + size // 4 + i * (size // 3)
            self.draw.line((dx, start_y, dx - 5, start_y + drop_len), fill=0, width=2)

    def draw_snow(self, x, y, size):
        """Draws a snow cloud."""
        self.draw_cloud(x, y, size)
        # Snowflakes (asterisks)
        start_y = y + size
        for i in range(3):
            dx = x + size // 4 + i * (size // 3)
            dy = start_y + size // 6
            r = 3
            self.draw.line((dx - r, dy, dx + r, dy), fill=0, width=1)
            self.draw.line((dx, dy - r, dx, dy + r), fill=0, width=1)
            self.draw.line((dx - r, dy - r, dx + r, dy + r), fill=0, width=1)
            self.draw.line((dx - r, dy + r, dx + r, dy - r), fill=0, width=1)

    def draw_storm(self, x, y, size):
        """Draws a storm cloud."""
        self.draw_cloud(x, y, size)
        # Lightning
        lx = x + size // 2
        ly = y + size
        points = [(lx, ly), (lx - 5, ly + 10), (lx + 5, ly + 10), (lx, ly + 20)]
        self.draw.line(points, fill=0, width=2)

    def draw_fog(self, x, y, size):
        """Draws fog lines."""
        for i in range(3):
            dy = y + size // 3 + i * (size // 4)
            self.draw.line((x, dy, x + size, dy), fill=0, width=2)

    def draw_sun_cloud(self, x, y, size):
        """Draws sun partially behind a cloud (Few Clouds)."""
        # Draw sun first (top right)
        r = size // 2
        cx, cy = x + r + (size//4), y + r - (size//4)
        # Core
        self.draw.ellipse((cx - r//2, cy - r//2, cx + r//2, cy + r//2), fill=0)
        # Rays (only top/right ones visible ideally, but drawing all is fine as cloud covers)
        ray_len = r // 3
        for i in range(0, 360, 45):
            import math
            rad = math.radians(i)
            x1 = cx + (r//2 + 2) * math.cos(rad)
            y1 = cy + (r//2 + 2) * math.sin(rad)
            x2 = cx + (r//2 + 2 + ray_len) * math.cos(rad)
            y2 = cy + (r//2 + 2 + ray_len) * math.sin(rad)
            self.draw.line((x1, y1, x2, y2), fill=0, width=2)
            
        # Draw cloud overlapping (bottom left)
        # Clear area for cloud first to simulate overlap
        cloud_size = int(size * 0.8)
        cx, cy = x, y + (size - cloud_size)
        
        # We need to "erase" the sun behind the cloud. 
        # Since we are drawing on 1-bit image with 0=black, 255=white.
        # We can draw a white cloud first, then black outline? 
        # Or just draw a white filled cloud shape over the sun, then draw the black cloud details.
        
        # Cloud shape parameters
        r = cloud_size // 3
        
        # Erase background (White fill)
        self.draw.ellipse((cx, cy + r, cx + 2*r, cy + 3*r), fill=255)
        self.draw.ellipse((cx + r, cy, cx + 3*r, cy + 2*r), fill=255)
        self.draw.ellipse((cx + 2*r, cy + r, cx + 4*r, cy + 3*r), fill=255)
        self.draw.rectangle((cx + r, cy + r, cx + 3*r, cy + 2.5*r), fill=255)
        
        # Draw Cloud Outline (Black)
        # To make it look good, we can just redraw the cloud using draw_cloud logic but slightly shifted
        self.draw_cloud(cx, cy, cloud_size)

    def draw_broken_clouds(self, x, y, size):
        """Draws two clouds (Overcast/Broken)."""
        # Back cloud (smaller, top right)
        self.draw_cloud(x + size//3, y, int(size*0.7))
        # Front cloud (normal, bottom left, with erase)
        
        cx, cy = x, y + size//4
        cloud_size = int(size * 0.8)
        r = cloud_size // 3
        
        # Erase
        self.draw.ellipse((cx, cy + r, cx + 2*r, cy + 3*r), fill=255)
        self.draw.ellipse((cx + r, cy, cx + 3*r, cy + 2*r), fill=255)
        self.draw.ellipse((cx + 2*r, cy + r, cx + 4*r, cy + 3*r), fill=255)
        self.draw.rectangle((cx + r, cy + r, cx + 3*r, cy + 2.5*r), fill=255)
        
        self.draw_cloud(cx, cy, cloud_size)

    def draw_shower_rain(self, x, y, size):
        """Draws cloud with heavy rain (Showers)."""
        self.draw_cloud(x, y, size)
        # Heavy rain: vertical lines
        drop_len = size // 3
        start_y = y + size
        for i in range(4):
            dx = x + size // 5 + i * (size // 4)
            self.draw.line((dx, start_y, dx, start_y + drop_len), fill=0, width=2)

    def draw_thunderstorm(self, x, y, size):
        """Draws cloud with lightning."""
        self.draw_cloud(x, y, size)
        # Lightning
        lx = x + size // 2
        ly = y + size
        # Zig-zag
        points = [(lx, ly), (lx - 8, ly + 15), (lx + 2, ly + 15), (lx - 5, ly + 30)]
        self.draw.line(points, fill=0, width=3)

    def draw_icon_for_code(self, code, x, y, size):
        """Maps WMO weather code to icon."""
        # Codes: https://open-meteo.com/en/docs
        # 0: Clear sky
        # 1, 2, 3: Mainly clear, partly cloudy, and overcast
        # 45, 48: Fog
        # 51, 53, 55: Drizzle
        # 56, 57: Freezing Drizzle
        # 61, 63, 65: Rain
        # 66, 67: Freezing Rain
        # 71, 73, 75: Snow fall
        # 77: Snow grains
        # 80, 81, 82: Rain showers
        # 85, 86: Snow showers
        # 95: Thunderstorm
        # 96, 99: Thunderstorm with hail

        if code == 0: # Clear sky -> Sun
            self.draw_sun(x, y, size)
        elif code == 1: # Mainly clear -> Sun + Cloud
            self.draw_sun_cloud(x, y, size)
        elif code == 2: # Partly cloudy -> Sun + Cloud
            self.draw_sun_cloud(x, y, size)
        elif code == 3: # Overcast -> Broken Clouds
            self.draw_broken_clouds(x, y, size)
        elif code in [45, 48]: # Fog
            self.draw_fog(x, y, size)
        elif code in [51, 53, 55, 56, 57]: # Drizzle -> Rain
            self.draw_rain(x, y, size)
        elif code in [61, 63, 65, 66, 67]: # Rain -> Rain
            self.draw_rain(x, y, size)
        elif code in [80, 81, 82]: # Rain showers -> Shower Rain
            self.draw_shower_rain(x, y, size)
        elif code in [71, 73, 75, 77, 85, 86]: # Snow
            self.draw_snow(x, y, size)
        elif code in [95, 96, 99]: # Thunderstorm
            self.draw_thunderstorm(x, y, size)
        else:
            self.draw_cloud(x, y, size) # Default

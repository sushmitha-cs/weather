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

    def draw_icon_for_code(self, code, x, y, size):
        """Maps WMO weather code to icon."""
        # Codes: https://open-meteo.com/en/docs
        if code == 0: # Clear sky
            self.draw_sun(x, y, size)
        elif code in [1, 2, 3]: # Partly cloudy
            self.draw_cloud(x, y, size) # Simplified to just cloud for now
        elif code in [45, 48]: # Fog
            self.draw_fog(x, y, size)
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: # Rain
            self.draw_rain(x, y, size)
        elif code in [71, 73, 75, 77, 85, 86]: # Snow
            self.draw_snow(x, y, size)
        elif code in [95, 96, 99]: # Thunderstorm
            self.draw_storm(x, y, size)
        else:
            self.draw_cloud(x, y, size) # Default

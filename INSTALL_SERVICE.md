# Installing Weather Display as a System Service

## Prerequisites
- Raspberry Pi with Raspbian/Raspberry Pi OS
- Weather display code installed in `/home/pi/weather_display`
- Python 3 and required dependencies installed

## Installation Steps

### 1. Update the Service File
Edit `weather-display.service` if needed to match your setup:
- Change `User=pi` if using a different username
- Update `WorkingDirectory=/home/pi/weather_display` to match your installation path

### 2. Copy Service File
```bash
sudo cp weather-display.service /etc/systemd/system/
```

### 3. Set Permissions
```bash
sudo chmod 644 /etc/systemd/system/weather-display.service
```

### 4. Reload Systemd
```bash
sudo systemctl daemon-reload
```

### 5. Enable Service (Start on Boot)
```bash
sudo systemctl enable weather-display.service
```

### 6. Start Service
```bash
sudo systemctl start weather-display.service
```

## Managing the Service

### Check Status
```bash
sudo systemctl status weather-display.service
```

### View Logs
```bash
# View recent logs
sudo journalctl -u weather-display.service -n 50

# Follow logs in real-time
sudo journalctl -u weather-display.service -f

# View logs since last boot
sudo journalctl -u weather-display.service -b
```

### Stop Service
```bash
sudo systemctl stop weather-display.service
```

### Restart Service
```bash
sudo systemctl restart weather-display.service
```

### Disable Service (Prevent Auto-Start)
```bash
sudo systemctl disable weather-display.service
```

## Troubleshooting

### Service Won't Start
1. Check the logs: `sudo journalctl -u weather-display.service -n 100`
2. Verify the working directory exists and contains the code
3. Ensure Python dependencies are installed
4. Check file permissions

### Permission Issues
If you get SPI/GPIO permission errors, you may need to add the user to the `spi` and `gpio` groups:
```bash
sudo usermod -a -G spi,gpio pi
```

### Network Dependency
The service waits for network connectivity before starting. If you experience issues:
- Check network status: `systemctl status network-online.target`
- Verify internet connectivity: `ping -c 4 8.8.8.8`

## Notes
- The service automatically restarts if it crashes (RestartSec=10)
- Logs are sent to systemd journal (viewable with `journalctl`)
- The service starts after network is available to ensure API access

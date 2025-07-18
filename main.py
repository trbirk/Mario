import hub75
import ntptime
import network
import time
import machine

# Wi-Fi credentials
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# HUB75 matrix configuration
WIDTH = 64
HEIGHT = 64
matrix = hub75.Hub75(WIDTH, HEIGHT)

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Set the time from NTP
try:
    ntptime.settime()
except Exception as e:
    print("Error setting time: " + str(e))

# Main loop
while True:
    # Get the current time
    now = time.localtime()
    hour = now[3]
    minute = now[4]
    second = now[5]

    # Format the time
    time_str = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)

    # Clear the display
    matrix.clear()

    # Draw the time
    matrix.text(time_str, 0, 0)

    # Update the display
    matrix.flip()

    # Wait for a second
    time.sleep(1)

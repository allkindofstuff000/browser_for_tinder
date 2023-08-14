import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import os
from timezonefinder import TimezoneFinder
from datetime import datetime
from selenium import webdriver
import pytz

# Rest of the code...

# Generate a random MAC address
def generate_random_mac_address():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Generate a random computer name
def generate_random_computer_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Function to get time zone based on SOCKS5 proxy IP
def get_timezone_from_ip(proxy_ip):
    geolocation_url = f"https://ipapi.co/{proxy_ip}/json/"
    response = requests.get(geolocation_url)
    if response.status_code == 200:
        data = response.json()
        latitude = data["latitude"]
        longitude = data["longitude"]
        tf = TimezoneFinder()
        timezone_name = tf.timezone_at(lng=longitude, lat=latitude)
        if timezone_name:
            timezone = pytz.timezone(timezone_name)
            now = datetime.now(timezone)
            timezone_abbreviation = now.strftime('%Z')
            timezone_offset = now.strftime('%z')
            return (timezone_name, timezone_abbreviation, timezone_offset)
    return None

# Prompt for SOCKS5 proxy IP and port
proxy_ip_port = input("Enter SOCKS5 proxy IP and port (e.g., 66.29.128.242:17321): ")

# Get time zone from SOCKS5 proxy IP
timezone = get_timezone_from_ip(proxy_ip_port.split(":")[0])

if timezone:
    timezone_name, timezone_abbreviation, timezone_offset = timezone
    print(f"Time zone set: {timezone_name} ({timezone_abbreviation}, UTC{timezone_offset})")
else:
    print("Failed to retrieve time zone.")

# Prompt for the Chrome profile directories
profile_directories = input("Enter the Chrome profile directories (comma-separated): ").split(",")

# Create the profile directories if they don't exist
for directory in profile_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Read the user agents from the text file
user_agents_file = r"C:\Users\main pc\Desktop\ALLSET\all user agent.txt"
with open(user_agents_file, "r") as file:
    user_agents = file.read().splitlines()

# Rest of the code...
for profile_directory in profile_directories:
    # Print the generated MAC address, computer name, and user agent
    mac_address = generate_random_mac_address()
    computer_name = generate_random_computer_name()
    user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    print("Generated MAC address:", mac_address)
    print("Generated computer name:", computer_name)
    print("Selected user agent:", user_agent)
    # Set the executable path to the Chromium browser
    executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.binary_location = executable_path
    chrome_options.add_argument(f'--user-data-dir={profile_directory}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-webrtc')
    chrome_options.add_argument('--disable-features=WebRtcHideLocalIpsWithMdns')
    chrome_options.add_argument('--disable-features=WebRtcLocalIpsWithMdns')
    chrome_options.add_argument('--disable-geolocation')
    chrome_options.add_argument(f'--user-agent={user_agent}')
    chrome_options.add_argument('--window-size=375,812')  # Adjust the width and height as needed
    chrome_options.add_argument('--window-position=0,0')  # Set the window position to top left
    # Set the SOCKS5 proxy
    chrome_options.add_argument(f'--proxy-server=socks5://{proxy_ip_port}')
    chrome_options.add_argument(f'--host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE {proxy_ip_port}"')
    chrome_options.add_argument(f'--host-rules="MAP * ~NOTFOUND , EXCLUDE {proxy_ip_port}"')

    # Set up the Chrome driver with custom options and executable path
    driver = uc.Chrome(options=chrome_options, executable_path=executable_path)

    # Maximize the window
    driver.maximize_window()

    # Set the browser window size to a specific width and height
    driver.set_window_size(500, 800)  # Adjust the width and height as needed


    # Wait for user action before closing the browser
input("Press Enter to close the browser...")
driver.quit()
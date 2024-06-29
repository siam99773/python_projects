import pywifi
import time
import logging
from pywifi import const

# Configure logging
logging.basicConfig(level=logging.INFO)

def connect_to_wifi(ssid, password):
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        logging.info("Disconnecting from WiFi...")
        iface.disconnect()
        time.sleep(1)
        assert iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

        logging.info(f"Connecting to WiFi network '{ssid}'...")
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)
        time.sleep(30)
        assert iface.status() == const.IFACE_CONNECTED
        logging.info("Connected to WiFi successfully!")

        # Optional: Scan and print nearby WiFi networks
        scan_and_print_networks(iface)

        logging.info("Disconnecting from WiFi...")
        iface.disconnect()
        time.sleep(1)
        assert iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        logging.info("Disconnected successfully!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def scan_and_print_networks(iface):
    try:
        logging.info("Scanning nearby WiFi networks...")
        wifi_scan_results = iface.scan_results()
        logging.info("Available WiFi Networks:")
        for wifi_network in wifi_scan_results:
            logging.info(f"SSID: {wifi_network.ssid}, Signal Strength: {wifi_network.signal}")
    except Exception as e:
        logging.error(f"Error occurred during WiFi scan: {e}")

# Example usage:
if __name__ == "__main__":
    ssid = input("Enter WiFi SSID: ")
    password = input("Enter WiFi password: ")

    connect_to_wifi(ssid, password)

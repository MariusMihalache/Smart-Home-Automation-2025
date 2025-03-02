import requests
import time
from datetime import datetime

# Detaliile API Home Assistant
home_assistant_url = 'http://192.168.1.100:8123/api/services/climate/set_temperature'
access_token = 'your_long_lived_access_token'

# Temperatura dorită (în grade Celsius)
desired_temperature = 22  # Temperatură confortabilă

# Funcție pentru verificarea prezenței
def check_presence():
    # Endpoint-ul pentru prezența utilizatorilor (ex: senzor de mișcare, tracker de GPS)
    presence_url = 'http://192.168.1.100:8123/api/states/device_tracker.phone'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(presence_url, headers=headers)
    if response.status_code == 200:
        state = response.json()['state']
        return state == 'home'
    else:
        return False

# Funcție pentru setarea temperaturii
def set_temperature():
    if check_presence():
        payload = {
            'entity_id': 'climate.thermostat',
            'temperature': desired_temperature
        }
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        response = requests.post(home_assistant_url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Temperatura a fost setată la {desired_temperature}°C")
        else:
            print("Eroare la setarea temperaturii.")
    else:
        print("Utilizatorul nu este acasă, nu se schimbă temperatura.")

# Rulăm scriptul la intervale pentru a ajusta automat temperatura
if __name__ == '__main__':
    while True:
        current_hour = datetime.now().hour
        # Automatizare pe baza orei (ex: răcire dimineața, încălzire seara)
        if current_hour >= 6 and current_hour <= 8:  # Dimineața
            desired_temperature = 21
        elif current_hour >= 18 and current_hour <= 22:  # Seara
            desired_temperature = 24
        
        set_temperature()
        time.sleep(600)  # Rulăm la fiecare 10 minute

# hass-lupusec
Lupusec XT1 and XT2 module for HASSIO

Supported units:
- Lupusec XT1
- Lupusec XT2+

Supported & tested devices:
- Window / Door sensor
- Sirene
- Keypad

Untested units / devices:
- XT1+
- XT2
- Motion sensor
- Smoke sensor
- Water sensor
- Power switch


For more devices create an issue

configuration.yaml 

lupusec: <br>
  device: XT1|XT2+ <br>
  username: YOUR_USERNAME <br>
  password: YOUR_PASSWORD <br>
  ssl: true|false (default=true) <br>
  ssl_trust_unverified: true|false (default=false) <br>
  ip_address: YOUR_IP_ADDRESS <br>


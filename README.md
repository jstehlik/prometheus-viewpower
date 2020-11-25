# prometheus-viewpower

Collects UPS metrics from a ViewPower web interface.

Tested against ViewPowerHTML V1.03 SP5, with FSP Champ TW 2K connected over USB. 

### Configuration
Copy config.json.example as config.json and specify one or more endpoints with running ViewPower, for example:
```
{
    "targets": [
    {
        "url": "http://10.0.0.1:15178/ViewPower/"
    },
    {
        "url": "http://10.23.45.67:15178/ViewPower/"
    },
    ...
    ]
}
```

### How to run
#### Using docker
```
docker run --name prometheus-viewpower -d -p 5600:5600 -v config.json:/config.json jstehlik/prometheus-viewpower
```
#### Without docker
```
# Create a virtual environment
python3 -m venv .env
source .env/bin/activate

# Install requirements
pip install -r requirements.txt

# Set config location
export PROMETHEUS_VIEWPOWER_CONFIGFILE=/path/to/config.json

# Run gunicorn as web server (or switch for any wsgi server)
gunicorn -b :5600 --access-logfile - 'prometheus_viewpower:create_app()'
```

### Metrics
Metrics are available on **/metrics**, i.e. http://localhost:5600/metrics

Following metrics are available:
```
viewpower_battery_capacity - Total battery capacity (%)
viewpower_battery_remaintime - Battery remaining time (minutes)
viewpower_battery_voltage - Battery voltage (V)
viewpower_input_frequency - Input frequency (Hz)
viewpower_input_voltage - Input voltage (V)
viewpower_output_current - Output current (A)
viewpower_output_frequency - Output frequency (Hz)
viewpower_output_loadpercent - Output load percent (%)
viewpower_output_voltage - Output voltage (V)
viewpower_temperature - Temperature (°C/°F)
```
Metrics have these labels available:
```
deviceId - device's serial number
endpoint - url of ViewPower which controls this device
```
from socket import timeout
from urllib.error import HTTPError, URLError
from prometheus_client.metrics_core import GaugeMetricFamily
from flask import current_app
import json
import urllib.request
import urllib.parse


class ViewPowerCollector(object):
    def __init__(self, config):
        self._config = config

    def collect(self):
        metrics = {
            'batteryCapacity': GaugeMetricFamily('viewpower_battery_capacity', 'Total battery capacity (%)', labels=['deviceId', 'endpoint']),
            'batteryRemainTime': GaugeMetricFamily('viewpower_battery_remaintime', 'Battery remaining time (minutes)', labels=['deviceId', 'endpoint']),
            'batteryVoltage': GaugeMetricFamily('viewpower_battery_voltage', 'Battery voltage (V)', labels=['deviceId', 'endpoint']),
            'inputFrequency': GaugeMetricFamily('viewpower_input_frequency', 'Input frequency (Hz)', labels=['deviceId', 'endpoint']),
            'inputVoltage': GaugeMetricFamily('viewpower_input_voltage', 'Input voltage (V)', labels=['deviceId', 'endpoint']),
            'outputCurrent': GaugeMetricFamily('viewpower_output_current', 'Output current (A)', labels=['deviceId', 'endpoint']),
            'outputFrequency': GaugeMetricFamily('viewpower_output_frequency', 'Output frequency (Hz)', labels=['deviceId', 'endpoint']),
            'outputLoadPercent': GaugeMetricFamily('viewpower_output_loadpercent', 'Output load percent (%)', labels=['deviceId', 'endpoint']),
            'outputVoltage': GaugeMetricFamily('viewpower_output_voltage', 'Output voltage (V)', labels=['deviceId', 'endpoint']),
            'temperatureView': GaugeMetricFamily('viewpower_temperature', 'Temperature (°C/°F)', labels=['deviceId', 'endpoint'])
        }

        for target in self._config['targets']:
            url = urllib.parse.urljoin(target['url'], 'workstatus/reqMonitorData')
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    current_app.logger.info(f'Polling {url}')
                    json_data = json.loads(response.read())

                    device_id = json_data['workInfo']['deviceId']
                    for key in json_data['workInfo']:
                        if key in metrics:
                            metrics[key].add_metric([device_id, target['url']], json_data['workInfo'][key])
            except (HTTPError, URLError) as error:
                current_app.logger.error(f'Failed polling {url}: {error}')
            except timeout:
                current_app.logger.error(f'Timed out polling {url}')

        return metrics.values()

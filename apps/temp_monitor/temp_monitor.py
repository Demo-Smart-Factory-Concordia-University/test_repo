import os
import time
from openfactory.apps import OpenFactoryApp
from openfactory.assets import Asset, AssetAttribute
from openfactory.kafka import KSQLDBClient


class TemperatureMonitor(OpenFactoryApp):
    """
    An OpenFactory application that monitors a temperature sensor and evaluates
    the readings against normal and warning thresholds.

    This app subscribes to sample events from a temperature sensor, assesses the data,
    and updates a condition attribute accordingly.
    """

    TEMP_SENSOR_UUID: str = os.getenv('TEMP_SENSOR_UUID', 'VIRTUAL-TEMP-SENS')
    TEMP_NORMAL: float = float(os.getenv('TEMP_NORMAL', 20))
    TEMP_WARNING: float = float(os.getenv('TEMP_WARNING', 20.5))

    def __init__(self, ksqlClient: KSQLDBClient, bootstrap_servers: str, debug: bool = False) -> None:
        """
        Initializes the TemperatureMonitor application.

        Args:
            ksqlClient (KSQLDBClient): The client used to communicate with KSQLDB.
            bootstrap_servers (str): Kafka bootstrap server addresses.
            debug (bool, optional): Enables debug mode if True. Defaults to False.
        """
        super().__init__(self.TEMP_SENSOR_UUID + '-MONITOR',
                         ksqlClient=ksqlClient,
                         bootstrap_servers=bootstrap_servers)
        self.DEBUG = debug

        # Extra attributes of the app
        self.add_attribute('temp_sensor', AssetAttribute(
            self.TEMP_SENSOR_UUID,
            type='Events',
            tag='DeviceUuid'))

        # Temperature sensor to monitor
        self.temp = Asset(self.TEMP_SENSOR_UUID,
                          ksqlClient=ksqlClient,
                          bootstrap_servers=bootstrap_servers)

        # Add Condition attribute to sensor
        self.temp.add_attribute('Temp_cond',
                                AssetAttribute('UNAVAILABLE',
                                               type='Condition',
                                               tag='UNAVAILABLE'))

        # Subscribe to samples from the temperature sensor
        self.temp.subscribe_to_samples(self.on_temp_sample,
                                       self.TEMP_SENSOR_UUID + '-MONITOR')

    def on_temp_sample(self, msg_key: str, msg_value: dict) -> None:
        """
        Callback for handling new samples from the temperature sensor.

        Evaluates the incoming temperature value and updates the `Temp_cond` attribute
        of the sensor based on configured thresholds:
        - "Normal" if temperature ≤ TEMP_NORMAL
        - "Warning" if temperature ≤ TEMP_WARNING
        - "Fault" if temperature > TEMP_WARNING

        Also prints debug information if debugging is enabled.

        Args:
            msg_key (str): The key of the Kafka message (the sensor ID).
            msg_value (dict): The message payload containing sample data.
                              Expected keys: 'id' (str), 'value' (float or str).
        """
        if self.DEBUG:
            print(f"{msg_value['id']}: {msg_value['value']}")

        # Check Temperature value and enrich Temp Sensor stream
        if msg_value['id'] == 'Temp':
            if float(msg_value['value']) <= self.TEMP_NORMAL:
                if self.DEBUG:
                    print('Normal temperature')
                self.temp.add_attribute('Temp_cond',
                                        AssetAttribute('Temperature is normal',
                                                       type='Condition',
                                                       tag='Normal'))
            elif float(msg_value['value']) <= self.TEMP_WARNING:
                if self.DEBUG:
                    print('Temperature warning')
                self.temp.add_attribute('Temp_cond',
                                        AssetAttribute('Temperature is getting high. Check.',
                                                       type='Condition',
                                                       tag='Warning'))
            else:
                if self.DEBUG:
                    print('High temperature')
                self.temp.add_attribute('Temp_cond',
                                        AssetAttribute('DANGER temperature is too high',
                                                       type='Condition',
                                                       tag='Fault'))

    def app_event_loop_stopped(self) -> None:
        """
        Called automatically when the main application event loop is stopped.

        This method handles cleanup tasks such as stopping the temperature
        sensor's sample subscription to ensure a graceful shutdown.
        """
        print("Stopping Temperature sensor consumer thread ...")
        self.temp.stop_samples_subscription()

    def main_loop(self) -> None:
        """ Main loop of the App. """
        while True:
            time.sleep(1)


def str_to_bool(value: str) -> bool:
    """
    Converts a string to a boolean value.

    Interprets common truthy string values such as "true", "1", or "yes"
    (case-insensitive) as `True`. All other values return `False`.

    Args:
        value (str): The input string to evaluate.

    Returns:
        bool: `True` if the string represents a truthy value, otherwise `False`.
    """
    return str(value).lower() in ("true", "1", "yes")


app = TemperatureMonitor(
        ksqlClient=KSQLDBClient(
            ksqldb_url=os.environ.get("KSQLDB_URL_DEPLOY", "http://localhost:8088"),
            loglevel=os.environ.get("KSQLDB_LOG_LEVEL", "WARNING")),
        bootstrap_servers=os.environ.get("KAFKA_BROKER_DEPLOY", "localhost:9092"),
        debug=str_to_bool(os.environ.get("DEBUG", "True")))
app.run()

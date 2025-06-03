import time
from openfactory.apps import OpenFactoryApp
from openfactory.kafka import KSQLDBClient


class DemoApp(OpenFactoryApp):

    def main_loop(self):
        # For actual use case, add here your logic of the app
        print("I don't do anything useful in this example.")
        counter = 1
        while True:
            print(counter)
            counter += 1
            time.sleep(2)

    def app_event_loop_stopped(self):
        # Not absolutely required as already done by the `KSQLDBClient` class
        self.ksql.close()


app = DemoApp(
    app_uuid='DEMO-APP',
    ksqlClient=KSQLDBClient("http://ksqldb-server:8088"),
    bootstrap_servers="broker:29092"
)
app.run()

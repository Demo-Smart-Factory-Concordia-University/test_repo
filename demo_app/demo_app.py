import time
from openfactory.assets import Asset
from openfactory.kafka import KSQLDBClient

ksql = KSQLDBClient('http://localhost:8088')
temp = Asset('VIRTUAL-TEMP-SENS', ksqlClient=ksql)

print(temp.samples())
print(temp.Temp.value)


def on_sample(msg_key, msg_value):
    print(f"[Sample] [{msg_key}] {msg_value}")

temp.subscribe_to_samples(on_sample, 'temp_samples_group')

# run a main loop while subscriptions remain active
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping consumer threads ...")
    temp.stop_samples_subscription()
    print("Consumers stopped")
finally:
    ksql.close()

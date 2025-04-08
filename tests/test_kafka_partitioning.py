import unittest
from confluent_kafka import Producer, Consumer
import hashlib

# Assume this is your custom partition function (it could be in your module)
def get_partition_for_key(key, num_partitions):
    """ Calculate the partition number for a given key """
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % num_partitions

class TestKafkaPartitioning(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """ Set up Kafka producer and consumer before any tests are run """
        cls.producer = Producer({'bootstrap.servers': 'localhost:9092'})
        cls.consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'test-consumer-group',
            'auto.offset.reset': 'earliest'
        })
        cls.consumer.subscribe(['mytopic'])
    
    @classmethod
    def tearDownClass(cls):
        """ Clean up after all tests are run """
        cls.consumer.close()

    def test_partitioning_logic(self):
        """ Test that your custom partitioning logic matches Kafka's partitioning behavior """

        # Produce a message
        key = 'asset-1234'
        value = {'asset_uuid': 'asset-1234', 'status': 'active'}

        # Send the message to the topic
        self.producer.produce('mytopic', key=key, value=str(value).encode('utf-8'))
        self.producer.flush()

        # Get the topic metadata to fetch the number of partitions
        metadata = self.consumer.list_topics(timeout=10)
        num_partitions = len(metadata.topics['mytopic'].partitions)

        # Calculate partition manually using your partitioning function
        expected_partition = get_partition_for_key(key, num_partitions)

        # Consume the message (after some delay for Kafka to process)
        msg = self.consumer.poll(timeout=1.0)

        # Test: Ensure that the correct message was consumed from the correct partition
        self.assertIsNotNone(msg, "No message received")
        self.assertFalse(msg.error(), f"Error: {msg.error()}")
        self.assertEqual(msg.key().decode('utf-8'), key, "Message key does not match expected key")
        self.assertEqual(msg.partition(), expected_partition, "Partition does not match expected partition")

if __name__ == '__main__':
    unittest.main()

from accelerometer import Accelerometer
from sounds import Taunter
from consumer import KnockDetectingConsumer


reader = Accelerometer()
taunter = Taunter()
consumer = KnockDetectingConsumer(reader, taunter.taunt)

if __name__ == "__main__":
	consumer.loop()

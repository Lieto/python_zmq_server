import time
import zmq
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def customCallback(client, userdata, message):
    print("Received new message:")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("------------\n\n")


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


myMQTTClient = AWSIoTMQTTClient("Test")
myMQTTClient.configureEndpoint("a1ahtb9zu9sh0c.iot.eu-central-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/kuoppves/PycharmProjects/zmq_server/deviceSDK/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem",
                                  "/home/kuoppves/PycharmProjects/zmq_server/deviceSDK/552dc012f9-private.pem.key",
                                  "/home/kuoppves/PycharmProjects/zmq_server/deviceSDK/552dc012f9-certificate.pem.crt")

myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

myMQTTClient.connect()
myMQTTClient.subscribe("$aws/things/BrTest/shadow/update", 1, customCallback)
time.sleep(2)


#loopCount = 0

while True:

#    myMQTTClient.publish("$aws/things/BrTest/shadow/update", "New Message " + str(loopCount), 1)
#    loopCount += 1

    message = socket.recv()

    # Server should send message to AWS IoT
    print("Received request: %s" % message)

    myMQTTClient.publish("test", message, 1)

    time.sleep(1)

    socket.send(b"World")

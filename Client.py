"""
default host
broker test host
mqtt.eclipse.org
port 1883
"""
import Connection as conn
from packet_struct import *
from mqtt_packets import *
import queue

result = queue.Queue()


""" The Client class defines the behaviour of the user. """
class Client:

    def __init__(self, client_id, username=None, password=None, host_ip=None, qos=0):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__host_ip = host_ip
        self.__topic_publish = ""
        self.__message_publish = ""
        self.__topics = []
        self.__unsubscribe_topics = []
        self.__connection = conn.Connection()
        self.__is_connected = False
        self.__struct = packet_struct()
        self.__qos = qos

    """ Defining the connect action. """
    def connect(self):
        self.__connection.establish_connection()
        if self.__host_ip is not None:
            self.__connection.set_host_ip(self.__host_ip)

        connect_packet = Connect()
        connect_packet.set_username(self.__username)
        connect_packet.set_password(self.__password)
        connect_packet.set_qos(self.__qos)
        packet = connect_packet.parse()

        self.__connection.send(packet)  # Send the connect packet
        self.__struct.byte_code = self.__connection.receive(1024)  # Receive the response packet
        assert self.__struct.byte_code[0:1] == packet_fixed_header['CONNACK']
        """The received packet is an acknowledgement packet 
        and the bytes received do not contain the header identifier of the packet"""
        if self.__struct.byte_code[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            self.__is_connected = True
            self.__struct.message = "Connect: success."
            result.put(self.__struct)
        else:
            self.__struct.message = "Connect: failed."
            result.put(self.__struct)

    """ Defining the disconnect action. """
    def disconnect(self):
        disconnect_packet = Disconnect()
        packet = disconnect_packet.parse()
        self.__connection.send(packet)
        self.__connection.close()
        self.__is_connected = False

    """ Defining the publish action. """
    def publish(self):
        publish_packet = Publish()
        publish_packet.set_qos(self.__qos)
        publish_packet.set_topic(self.__topic_publish)
        publish_packet.set_message(self.__message_publish)

        packet = publish_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = b''  # self.__connection.receive(1024)
        # assert self.__struct.byte_code[0:1] == packet_fixed_header['PUBACK']
        if self.__struct.byte_code[-2:-1] == b'':
            self.__struct.message = "Publish: success."
            result.put(self.__struct)
        else:
            self.__struct.message = "Publish: failed."
            result.put(self.__struct)

    """ Defining the pingreq action. """
    def pingreq(self):
        pingreq_packet = PingReq()
        packet = pingreq_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = self.__connection.receive(1024)
        assert self.__struct.byte_code[0:1] == packet_fixed_header['PINGRESP']

    """ Defining the subscribe action. """
    def subscribe(self):
        subscribe_packet = Subscribe()
        subscribe_packet.set_topics(self.__topics)
        self.__topics = []
        packet = subscribe_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = self.__connection.receive(1024)
        assert self.__struct.byte_code[0:1] == packet_fixed_header['SUBACK']
        if self.__struct.byte_code[-1:] == b'\x01' or self.__struct.byte_code[-1:] == b'\x02' or self.__struct.byte_code[-1:] == b'\x00':
            self.__struct.message = "Subscribe: success.\n"
            result.put(self.__struct)
        else:
            self.__struct.message = "Subscribe: failed.\n"
            result.put(self.__struct)

    """ Defining the unsubscribe action. """
    def unsubscribe(self):
        unsubscribe_packet = Unsubscribe()
        unsubscribe_packet.set_topics(self.__unsubscribe_topics)
        self.__unsubscribe_topics = []
        packet = unsubscribe_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = self.__connection.receive(1024)
        assert self.__struct.byte_code[0:1] == packet_fixed_header['UNSUBACK']
        if self.__struct.byte_code[-1:] == b'\x00':
            self.__struct.message = "Unsubscribe: success.\n"
            result.put(self.__struct)
        else:
            self.__struct.message = "Unsubscribe failed.\n"
            result.put(self.__struct)

    def get_connection(self):
        return self.__connection

    """ Getter method for is_connected field. """
    def get_is_connected(self):
        return self.__is_connected

    """ Append method for the unsubscribe topics. """
    def add_unsubscribe_topic(self, _unsubscribe_topic):
        self.__unsubscribe_topics.append(_unsubscribe_topic)

    """ Append method for the list of topics. """
    def add_topic(self, _topic):
        self.__topics.append(_topic)

    def set_message_publish(self, _message):
        self.__message_publish = _message

    def set_topic_publish(self, _topic):
        self.__topic_publish = _topic

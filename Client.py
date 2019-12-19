"""
default host
broker test host
mqtt.eclipse.org
port 1883

CONNECT = 0x10
CONNACK = 0x20
PUBLISH = 0x30
PUBACK = 0x40
PUBREC = 0x50
PUBREL = 0x62
PUBCOMP = 0x70
SUBSCRIBE = 0x82
SUBACK = 0x90
UNSUBSCRIBE = 0xA2
UNSUBACK = 0xB0
PINGREQ = 0xC0
PINGRESP = 0xD0
DISCONNECT = 0xE0
AUTH = 0xF0
"""
import Connection as conn
import threading
CONNECT = b'\x10'
CONNACK = b'\x20'
PUBLISH = b'\x30'
PUBACK = b'\x40'
PUBREC = b'\x50'
PUBREL = b'\x62'
PUBCOMP = b'\x70'
SUBSCRIBE = b'\x82'
SUBACK = b'\x90'
UNSUBSCRIBE = b'\xA2'
UNSUBACK = b'\xB0'
PINGREQ = b'\xC0'
PINGRESP = b'\xD0'
DISCONNECT = b'\xE0'
AUTH = b'\xF0'


class Client:

    def __init__(self, client_id, topic=None, username=None, password=None):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__topic = topic
        self.__connection = conn.Connection()
        self.__socket = None
        self.__thread = None
        self.__protocol_name = "MQTT"
        self.__is_connected = False
        self.__packet_fields = {
            'protocol_name': "MQTT",
            'keep_alive': b'\x00\x05',  # keep alive
            'properties': b'\x11\x00\x00\x00\x0a',  # properties
            'connect_flags': b'\x02',  # connect flags
            'version': b'\5'
        }

    def connect(self):
        packet = bytearray()  # initialize the packet to be sent
        # connect_flags = b'\x02'  # connect flags
        # keep_alive = b'\x00\x05'  # keep alive
        # properties = b'\x11\x00\x00\x00\x0a'  # properties
        variable_header = bytearray()  # initialize an empty byte array to create the variable header
        packet += CONNECT
        variable_header += b'\x00'
        variable_header += bytes([len(self.__packet_fields['protocol_name'])])
        variable_header += self.__packet_fields['protocol_name'].encode('UTF-8')
        variable_header += self.__packet_fields['version']  # version 5
        variable_header += self.__packet_fields['connect_flags']
        variable_header += self.__packet_fields['keep_alive']
        variable_header += bytes([len(self.__packet_fields['properties'])])
        variable_header += self.__packet_fields['properties']
        variable_header += b'\x00'
        payload = bytes([len(self.__username)])
        payload += self.__username.encode('UTF-8')
        variable_header += payload

        packet_length = bytes([len(variable_header)])  # calculate the length of the remaining packet
        packet += packet_length  # add the length as bytes to the packet
        packet += variable_header  # add the whole variable_header to the packet
        self.__connection.send(packet)  # Send the connect packet
        received_packet = self.__connection.receive(1024)  # Receive the response packet
        print(repr(received_packet))
        """The received packet is an acknowledgement packet 
        and the bytes received do not contain the header identifier of the packet"""
        if received_packet[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            print("Connection acknowledged")
            self.__is_connected = True
        else:
            print("Connection dropped")

    def publish(self):
        pass

    def subscribe(self):
        pass

    def get_is_connected(self):
        return self.__is_connected

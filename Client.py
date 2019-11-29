"""
default host
broker test host
mqtt.eclipse.org
port 1883
"""
import Connection as conn


class Client(object):

    def __init__(self, client_id, topic=None, username=None, password=None, keep_alive=60, message_retry=20):
        self._username = username
        self._client_id = client_id
        self._password = password
        self._topic = topic
        self._connection = conn.Connection()
        self._keep_alive = keep_alive
        self._socket = None
        self._message_retry = message_retry
        self._in_packet = {
            "command": 0,
            "have_remaining": 0,
            "remaining_count": [],
            "remaining_mult": 0,
            "remaining_length": 0,
            "packet": b"",
            "pos": 0
        }
        self._thread = None

    def connect(self):
        packet = bytearray(b'\x10')
        protocol_name = "04MQTT"  # 04MQTT
        packet.extend(protocol_name.encode('UTF-8'))
        protocol_version = "05"  # version =5
        """connect_flags bits
        username flag=1
        password flag =1
        will retain = 0
        will qos=01
        will flag=1
        clean start=1
        reserved =0
        connect_flags = "CA"
        keep_alive = "000A"  # keep alive LSB=10
        proprieties = "05110"  # length = 5; session expiry interval =  10; session expiry interval identifier = 17
        """
        packet.extend(b'\xca\x00\x0a\x05\x11')

        #payload = self._client_id + self._username + self._password
        """
        variable_header = append_hex(messages.CONNECT, protocol_name)
        variable_header = append_hex(variable_header, protocol_version)
        variable_header = append_hex(variable_header, connect_flags)
        variable_header = append_hex(variable_header, keep_alive)
        variable_header = append_hex(variable_header, proprieties)
        packet = append_hex(variable_header, self._client_id)
        """
        #packet = protocol_name + protocol_version + connect_flags + keep_alive + proprieties + payload
        self._connection.send(packet)

    def publish(self, dup=False, qos=0x01, retain=False):
        """
        command = messages.PUBLISH << 4 | (dup & 0x1) << 3 | qos << 1 | retain
        command << 8
        packet = bytearray()
        packet.append(command)
        self._connection.send(packet)
        """

    def subscribe(self):
        pass
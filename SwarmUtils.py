import struct
import sys
import socket

class Swarm:
    def _create_parameters(self):
        # ограничение в 16 команд
        # можно обойти путем отправки пользовательских команд через параметры 1й команды
        (
            self.CMD_USER_COMMAND,
            self.CMD_ARM,
            self.CMD_DISARM,
            self.CMD_LOCAL_MOVE,
            self.CMD_ABSOLUTE_MOVE,
            self.CMD_SET_LED_STATE
        ) = [i for i in range(6)]

    def get_unpacking_parameter(self, start_byte):
        data_command = (start_byte & 0b11110000) >> 4

        if data_command == self.CMD_USER_COMMAND:
            return "8s"
        elif data_command == self.CMD_ARM:
            return "x"
        elif data_command == self.CMD_DISARM:
            return "x"
        elif data_command == self.CMD_LOCAL_MOVE:
            return "bi"
        elif data_command == self.CMD_ABSOLUTE_MOVE:
            return "cicici"
        elif data_command == self.CMD_SET_LED_STATE:
            return "BBB"


class SwarmServer(Swarm):
    def __init__(self, server_ip='localhost', server_port=9090):
        self._create_parameters()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.settimeout(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((server_ip, server_port))

    def send_command(self, cmd, data, ip='<broadcast>', port=9091):
        start_byte = (cmd << 4) + len(data)

        print(bin(cmd), bin(len(data)), bin(start_byte))

        # packline = 'b' + self.get_unpacking_parameter(start_byte)

        self.socket.sendto(struct.pack('b', start_byte), (ip, port))

        self.socket.sendto(struct.pack(self.get_unpacking_parameter(start_byte), *data), (ip, port))

        # self.socket.sendto(struct.pack(
        #     packline,
        #     start_byte, *data
        # ), (ip, port))

    def receive_command(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                print(data, " from ", addr)
            except Exception:
                pass




class SwarmClient(Swarm):
    def __init__(self, server_ip='localhost', server_port=9090, client_ip='localhost', client_port=9091):
        self._create_parameters()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.settimeout(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((client_ip, client_port))
        self.socket.connect((server_ip, server_port))
        self.socket.send(struct.pack('4s', b'test'))

    def send_command(self, cmd, data, ip='<broadcast>', port=9091):
        start_byte = (cmd << 4) + len(data)

        print(bin(cmd), bin(len(data)), bin(start_byte))

        # packline = 'b' + self.get_unpacking_parameter(start_byte)

        self.socket.sendto(struct.pack('b', start_byte), (ip, port))

        self.socket.sendto(struct.pack(self.get_unpacking_parameter(start_byte), *data), (ip, port))

    def receive_data(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1)
                start_byte = struct.unpack('b', data)[0]
                data_len = start_byte & 0b00001111
                if data:
                    payload, _ = self.socket.recvfrom(data_len)
                    payload = struct.unpack(self.get_unpacking_parameter(start_byte), payload)
                    print("Received data from ", addr, ": ", start_byte, payload)
                    # break
            except Exception as e:
                print(e)
